#include "TextService.h"
#include <algorithm>
#include <cstdio>
#include <new>
#include <vector>

static std::wstring GetPipeNameForProcess(DWORD processId)
{
    wchar_t pipeName[128] = {};
    swprintf_s(pipeName, ARRAYSIZE(pipeName), L"\\\\.\\pipe\\uclliu_tsf_bridge_%lu", processId);
    return pipeName;
}

static std::wstring Utf8ToWide(const std::string& text)
{
    if (text.empty())
    {
        return std::wstring();
    }
    int chars = MultiByteToWideChar(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), nullptr, 0);
    if (chars <= 0)
    {
        return std::wstring();
    }
    std::wstring output(chars, L'\0');
    MultiByteToWideChar(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), &output[0], chars);
    return output;
}

static std::string JsonEscape(const std::string& text)
{
    std::string out;
    out.reserve(text.size() + 8);
    for (char ch : text)
    {
        switch (ch)
        {
        case '\\': out += "\\\\"; break;
        case '"': out += "\\\""; break;
        case '\r': out += "\\r"; break;
        case '\n': out += "\\n"; break;
        default: out += ch; break;
        }
    }
    return out;
}

static bool ExtractJsonString(const std::string& request, const std::string& key, std::string& value)
{
    const std::string marker = "\"" + key + "\"";
    size_t pos = request.find(marker);
    if (pos == std::string::npos)
    {
        return false;
    }
    pos = request.find(':', pos + marker.size());
    if (pos == std::string::npos)
    {
        return false;
    }
    pos = request.find('"', pos + 1);
    if (pos == std::string::npos)
    {
        return false;
    }
    ++pos;

    std::string out;
    bool escaping = false;
    for (; pos < request.size(); ++pos)
    {
        char ch = request[pos];
        if (escaping)
        {
            switch (ch)
            {
            case 'n': out += '\n'; break;
            case 'r': out += '\r'; break;
            case 't': out += '\t'; break;
            default: out += ch; break;
            }
            escaping = false;
            continue;
        }
        if (ch == '\\')
        {
            escaping = true;
            continue;
        }
        if (ch == '"')
        {
            value = out;
            return true;
        }
        out += ch;
    }
    return false;
}

static DWORD WINAPI PipeThreadProc(void* param)
{
    static_cast<UclTextService*>(param)->AddRef();
    static_cast<UclTextService*>(param)->PipeLoop();
    static_cast<UclTextService*>(param)->Release();
    return 0;
}

UclEditSession::UclEditSession(UclTextService* owner, ITfContext* context, const std::wstring& text)
    : _owner(owner), _context(context), _text(text)
{
    DllAddRef();
    if (_owner)
    {
        _owner->AddRef();
    }
    if (_context)
    {
        _context->AddRef();
    }
}

STDMETHODIMP UclEditSession::QueryInterface(REFIID riid, void** ppvObject)
{
    if (!ppvObject)
    {
        return E_INVALIDARG;
    }
    *ppvObject = nullptr;
    if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_ITfEditSession))
    {
        *ppvObject = static_cast<ITfEditSession*>(this);
        AddRef();
        return S_OK;
    }
    return E_NOINTERFACE;
}

STDMETHODIMP_(ULONG) UclEditSession::AddRef()
{
    return ++_refCount;
}

STDMETHODIMP_(ULONG) UclEditSession::Release()
{
    long count = --_refCount;
    if (count == 0)
    {
        if (_context)
        {
            _context->Release();
        }
        if (_owner)
        {
            _owner->Release();
        }
        DllRelease();
        delete this;
    }
    return count;
}

STDMETHODIMP UclEditSession::DoEditSession(TfEditCookie ec)
{
    return _owner ? _owner->InsertText(_context, ec, _text) : E_FAIL;
}

UclTextService::UclTextService()
{
    DllAddRef();
}

UclTextService::~UclTextService()
{
    StopPipeServer();
    if (_focusContext)
    {
        _focusContext->Release();
        _focusContext = nullptr;
    }
    if (_threadMgr)
    {
        _threadMgr->Release();
        _threadMgr = nullptr;
    }
    DllRelease();
}

STDMETHODIMP UclTextService::QueryInterface(REFIID riid, void** ppvObject)
{
    if (!ppvObject)
    {
        return E_INVALIDARG;
    }
    *ppvObject = nullptr;

    if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_ITfTextInputProcessor))
    {
        *ppvObject = static_cast<ITfTextInputProcessor*>(this);
    }
    else if (IsEqualIID(riid, IID_ITfThreadMgrEventSink))
    {
        *ppvObject = static_cast<ITfThreadMgrEventSink*>(this);
    }
    else if (IsEqualIID(riid, IID_ITfKeyEventSink))
    {
        *ppvObject = static_cast<ITfKeyEventSink*>(this);
    }
    else
    {
        return E_NOINTERFACE;
    }

    AddRef();
    return S_OK;
}

STDMETHODIMP_(ULONG) UclTextService::AddRef()
{
    return ++_refCount;
}

STDMETHODIMP_(ULONG) UclTextService::Release()
{
    long count = --_refCount;
    if (count == 0)
    {
        delete this;
    }
    return count;
}

STDMETHODIMP UclTextService::Activate(ITfThreadMgr* threadMgr, TfClientId clientId)
{
    if (!threadMgr)
    {
        return E_INVALIDARG;
    }
    _threadMgr = threadMgr;
    _threadMgr->AddRef();
    _clientId = clientId;
    AdviseSinks();
    ITfDocumentMgr* docMgr = nullptr;
    if (SUCCEEDED(_threadMgr->GetFocus(&docMgr)) && docMgr)
    {
        // 啟用時焦點可能已經在文字框內，先補抓一次目前 context。
        UpdateFocusContext(docMgr);
        docMgr->Release();
    }
    StartPipeServer();
    return S_OK;
}

STDMETHODIMP UclTextService::Deactivate()
{
    StopPipeServer();
    UnadviseSinks();

    std::lock_guard<std::mutex> lock(_contextMutex);
    if (_focusContext)
    {
        _focusContext->Release();
        _focusContext = nullptr;
    }
    if (_threadMgr)
    {
        _threadMgr->Release();
        _threadMgr = nullptr;
    }
    _clientId = TF_CLIENTID_NULL;
    return S_OK;
}

void UclTextService::AdviseSinks()
{
    ITfSource* source = nullptr;
    if (_threadMgr && SUCCEEDED(_threadMgr->QueryInterface(IID_ITfSource, reinterpret_cast<void**>(&source))))
    {
        source->AdviseSink(IID_ITfThreadMgrEventSink, static_cast<ITfThreadMgrEventSink*>(this), &_threadMgrSinkCookie);
        source->Release();
    }

    ITfKeystrokeMgr* keyMgr = nullptr;
    if (_threadMgr && SUCCEEDED(_threadMgr->QueryInterface(IID_ITfKeystrokeMgr, reinterpret_cast<void**>(&keyMgr))))
    {
        _keySinkAdvised = SUCCEEDED(keyMgr->AdviseKeyEventSink(_clientId, static_cast<ITfKeyEventSink*>(this), TRUE));
        keyMgr->Release();
    }
}

void UclTextService::UnadviseSinks()
{
    ITfKeystrokeMgr* keyMgr = nullptr;
    if (_keySinkAdvised && _threadMgr && SUCCEEDED(_threadMgr->QueryInterface(IID_ITfKeystrokeMgr, reinterpret_cast<void**>(&keyMgr))))
    {
        keyMgr->UnadviseKeyEventSink(_clientId);
        keyMgr->Release();
    }
    _keySinkAdvised = false;

    ITfSource* source = nullptr;
    if (_threadMgrSinkCookie != TF_INVALID_COOKIE && _threadMgr && SUCCEEDED(_threadMgr->QueryInterface(IID_ITfSource, reinterpret_cast<void**>(&source))))
    {
        source->UnadviseSink(_threadMgrSinkCookie);
        source->Release();
    }
    _threadMgrSinkCookie = TF_INVALID_COOKIE;
}

STDMETHODIMP UclTextService::OnInitDocumentMgr(ITfDocumentMgr*) { return S_OK; }
STDMETHODIMP UclTextService::OnUninitDocumentMgr(ITfDocumentMgr*) { return S_OK; }

STDMETHODIMP UclTextService::OnSetFocus(ITfDocumentMgr* docMgrFocus, ITfDocumentMgr*)
{
    UpdateFocusContext(docMgrFocus);
    return S_OK;
}

STDMETHODIMP UclTextService::OnPushContext(ITfContext* context)
{
    SetFocusContext(context);
    return S_OK;
}

STDMETHODIMP UclTextService::OnPopContext(ITfContext*)
{
    ITfDocumentMgr* docMgr = nullptr;
    if (_threadMgr && SUCCEEDED(_threadMgr->GetFocus(&docMgr)))
    {
        UpdateFocusContext(docMgr);
        docMgr->Release();
    }
    return S_OK;
}

void UclTextService::UpdateFocusContext(ITfDocumentMgr* docMgr)
{
    ITfContext* context = nullptr;
    if (docMgr)
    {
        docMgr->GetTop(&context);
    }
    SetFocusContext(context);
    if (context)
    {
        context->Release();
    }
}

void UclTextService::SetFocusContext(ITfContext* context)
{
    std::lock_guard<std::mutex> lock(_contextMutex);
    if (_focusContext)
    {
        _focusContext->Release();
    }
    _focusContext = context;
    if (_focusContext)
    {
        _focusContext->AddRef();
    }
}

STDMETHODIMP UclTextService::OnSetFocus(BOOL) { return S_OK; }
STDMETHODIMP UclTextService::OnTestKeyDown(ITfContext* context, WPARAM, LPARAM, BOOL* eaten) { SetFocusContext(context); if (eaten) *eaten = FALSE; return S_OK; }
STDMETHODIMP UclTextService::OnKeyDown(ITfContext* context, WPARAM, LPARAM, BOOL* eaten) { SetFocusContext(context); if (eaten) *eaten = FALSE; return S_OK; }
STDMETHODIMP UclTextService::OnTestKeyUp(ITfContext* context, WPARAM, LPARAM, BOOL* eaten) { SetFocusContext(context); if (eaten) *eaten = FALSE; return S_OK; }
STDMETHODIMP UclTextService::OnKeyUp(ITfContext* context, WPARAM, LPARAM, BOOL* eaten) { SetFocusContext(context); if (eaten) *eaten = FALSE; return S_OK; }
STDMETHODIMP UclTextService::OnPreservedKey(ITfContext*, REFGUID, BOOL* eaten) { if (eaten) *eaten = FALSE; return S_OK; }

bool UclTextService::HasContext()
{
    std::lock_guard<std::mutex> lock(_contextMutex);
    return _focusContext != nullptr;
}

HRESULT UclTextService::CommitText(const std::wstring& text)
{
    ITfContext* context = nullptr;
    {
        std::lock_guard<std::mutex> lock(_contextMutex);
        context = _focusContext;
        if (context)
        {
            context->AddRef();
        }
    }

    if (!context)
    {
        return HRESULT_FROM_WIN32(ERROR_INVALID_STATE);
    }

    auto* session = new (std::nothrow) UclEditSession(this, context, text);
    context->Release();
    if (!session)
    {
        return E_OUTOFMEMORY;
    }

    HRESULT sessionResult = E_FAIL;
    // 這裡要同步完成，否則 pipe 會先回覆成功/失敗，實際 commit 卻還沒跑完。
    HRESULT hr = context->RequestEditSession(_clientId, session, TF_ES_READWRITE | TF_ES_SYNC, &sessionResult);
    session->Release();
    return SUCCEEDED(hr) ? sessionResult : hr;
}

HRESULT UclTextService::InsertText(ITfContext* context, TfEditCookie ec, const std::wstring& text)
{
    if (!context)
    {
        return E_INVALIDARG;
    }

    ITfInsertAtSelection* insertAtSelection = nullptr;
    HRESULT hr = context->QueryInterface(IID_ITfInsertAtSelection, reinterpret_cast<void**>(&insertAtSelection));
    if (FAILED(hr))
    {
        return hr;
    }

    hr = insertAtSelection->InsertTextAtSelection(
        ec,
        TF_IAS_NOQUERY,
        text.c_str(),
        static_cast<LONG>(text.size()),
        nullptr);
    insertAtSelection->Release();
    return hr;
}

void UclTextService::StartPipeServer()
{
    if (_pipeThread)
    {
        return;
    }
    _pipeStopEvent = CreateEventW(nullptr, TRUE, FALSE, nullptr);
    if (!_pipeStopEvent)
    {
        return;
    }
    _pipeThread = CreateThread(nullptr, 0, PipeThreadProc, this, 0, nullptr);
}

void UclTextService::StopPipeServer()
{
    if (_pipeStopEvent)
    {
        SetEvent(_pipeStopEvent);
    }
    if (_pipeThread)
    {
        WaitForSingleObject(_pipeThread, 1000);
        CloseHandle(_pipeThread);
        _pipeThread = nullptr;
    }
    if (_pipeStopEvent)
    {
        CloseHandle(_pipeStopEvent);
        _pipeStopEvent = nullptr;
    }
}

void UclTextService::PipeLoop()
{
    CoInitializeEx(nullptr, COINIT_MULTITHREADED);
    DWORD processId = GetCurrentProcessId();
    // 每個前景程序各自使用獨立 pipe，避免 Python 連到別的 TSF instance。
    std::wstring pipeName = GetPipeNameForProcess(processId);
    while (_pipeStopEvent && WaitForSingleObject(_pipeStopEvent, 0) == WAIT_TIMEOUT)
    {
        HANDLE pipe = CreateNamedPipeW(
            pipeName.c_str(),
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            1,
            8192,
            8192,
            100,
            nullptr);

        if (pipe == INVALID_HANDLE_VALUE)
        {
            Sleep(250);
            continue;
        }

        BOOL connected = ConnectNamedPipe(pipe, nullptr) ? TRUE : (GetLastError() == ERROR_PIPE_CONNECTED);
        if (connected)
        {
            char buffer[8192] = {};
            DWORD bytesRead = 0;
            if (ReadFile(pipe, buffer, sizeof(buffer) - 1, &bytesRead, nullptr) && bytesRead > 0)
            {
                std::string response = HandlePipeRequest(std::string(buffer, bytesRead));
                DWORD bytesWritten = 0;
                WriteFile(pipe, response.data(), static_cast<DWORD>(response.size()), &bytesWritten, nullptr);
            }
        }

        FlushFileBuffers(pipe);
        DisconnectNamedPipe(pipe);
        CloseHandle(pipe);
    }
    CoUninitialize();
}

std::string UclTextService::HandlePipeRequest(const std::string& request)
{
    std::string cmd;
    if (!ExtractJsonString(request, "cmd", cmd))
    {
        return "{\"ok\":false,\"error\":\"BAD_REQUEST\"}\n";
    }

    if (cmd == "ping")
    {
        return "{\"ok\":true,\"pong\":true}\n";
    }
    if (cmd == "status")
    {
        return HasContext()
            ? "{\"ok\":true,\"active\":true,\"has_context\":true}\n"
            : "{\"ok\":true,\"active\":true,\"has_context\":false}\n";
    }
    if (cmd == "commit_text")
    {
        std::string textUtf8;
        if (!ExtractJsonString(request, "text", textUtf8))
        {
            return "{\"ok\":false,\"error\":\"NO_TEXT\"}\n";
        }

        HRESULT hr = CommitText(Utf8ToWide(textUtf8));
        if (SUCCEEDED(hr))
        {
            return "{\"ok\":true}\n";
        }

        char response[128] = {};
        sprintf_s(response, "{\"ok\":false,\"error\":\"COMMIT_FAILED\",\"hr\":\"0x%08X\"}\n", static_cast<unsigned int>(hr));
        return response;
    }

    return "{\"ok\":false,\"error\":\"UNKNOWN_CMD\"}\n";
}

STDMETHODIMP UclClassFactory::QueryInterface(REFIID riid, void** ppvObject)
{
    if (!ppvObject)
    {
        return E_INVALIDARG;
    }
    *ppvObject = nullptr;
    if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_IClassFactory))
    {
        *ppvObject = static_cast<IClassFactory*>(this);
        AddRef();
        return S_OK;
    }
    return E_NOINTERFACE;
}

UclClassFactory::UclClassFactory()
{
    DllAddRef();
}

UclClassFactory::~UclClassFactory()
{
    DllRelease();
}

STDMETHODIMP_(ULONG) UclClassFactory::AddRef()
{
    return ++_refCount;
}

STDMETHODIMP_(ULONG) UclClassFactory::Release()
{
    long count = --_refCount;
    if (count == 0)
    {
        delete this;
    }
    return count;
}

STDMETHODIMP UclClassFactory::CreateInstance(IUnknown* outer, REFIID riid, void** ppvObject)
{
    if (outer)
    {
        return CLASS_E_NOAGGREGATION;
    }
    auto* service = new (std::nothrow) UclTextService();
    if (!service)
    {
        return E_OUTOFMEMORY;
    }
    HRESULT hr = service->QueryInterface(riid, ppvObject);
    service->Release();
    return hr;
}

STDMETHODIMP UclClassFactory::LockServer(BOOL lock)
{
    if (lock)
    {
        DllAddRef();
    }
    else
    {
        DllRelease();
    }
    return S_OK;
}
