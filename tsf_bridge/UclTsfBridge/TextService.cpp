#include "TextService.h"
#include <algorithm>
#include <cstdio>
#include <new>
#include <vector>
#include <mutex>

#define WM_UCL_COMMIT (WM_USER + 100)

static std::atomic<UclTextService*> g_pActiveService{ nullptr };
static std::mutex g_pipeMutex;
static HANDLE g_hPipeThread = nullptr;
static HANDLE g_hPipeStopEvent = nullptr;
static DWORD g_pipeThreadId = 0;
static std::atomic<UclTextService*> g_pPipeService{ nullptr };

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

static bool WideEqualsIgnoreCase(const wchar_t* lhs, const wchar_t* rhs)
{
    return CompareStringOrdinal(lhs, -1, rhs, -1, TRUE) == CSTR_EQUAL;
}

static const wchar_t* FileNameFromPath(const wchar_t* path)
{
    const wchar_t* fileName = path;
    for (const wchar_t* p = path; p && *p; ++p)
    {
        if (*p == L'\\' || *p == L'/')
        {
            fileName = p + 1;
        }
    }
    return fileName;
}

static bool IsBadHostProcess()
{
    wchar_t modulePath[MAX_PATH] = {};
    DWORD length = GetModuleFileNameW(nullptr, modulePath, ARRAYSIZE(modulePath));
    if (length == 0 || length >= ARRAYSIZE(modulePath))
    {
        return false;
    }

    const wchar_t* processName = FileNameFromPath(modulePath);
    static constexpr const wchar_t* kBadHosts[] = {
        L"explorer.exe",
        L"OpenWith.exe",
        L"PickerHost.exe",
        L"FilePicker.exe",
        L"FileOpenPicker.exe",
        L"SearchHost.exe",
        L"ShellExperienceHost.exe",
        L"StartMenuExperienceHost.exe",
        L"LINE.exe",
        L"msedgewebview2.exe",
    };

    for (const wchar_t* badHost : kBadHosts)
    {
        if (WideEqualsIgnoreCase(processName, badHost))
        {
            return true;
        }
    }
    return false;
}

static bool WindowClassEquals(HWND hwnd, const wchar_t* className)
{
    wchar_t actualClassName[128] = {};
    if (!hwnd || !GetClassNameW(hwnd, actualClassName, ARRAYSIZE(actualClassName)))
    {
        return false;
    }
    return WideEqualsIgnoreCase(actualClassName, className);
}

static bool HasDescendantWindowClass(HWND hwnd, const wchar_t* className, int depth = 0)
{
    if (!hwnd || depth > 10)
    {
        return false;
    }

    for (HWND child = GetWindow(hwnd, GW_CHILD); child; child = GetWindow(child, GW_HWNDNEXT))
    {
        if (WindowClassEquals(child, className) || HasDescendantWindowClass(child, className, depth + 1))
        {
            return true;
        }
    }
    return false;
}

static bool IsShellFileDialogWindow(HWND hwnd)
{
    if (WindowClassEquals(hwnd, L"CabinetWClass") || WindowClassEquals(hwnd, L"ExploreWClass"))
    {
        return true;
    }

    if (!WindowClassEquals(hwnd, L"#32770"))
    {
        return false;
    }

    if (HasDescendantWindowClass(hwnd, L"SHELLDLL_DefView") ||
        HasDescendantWindowClass(hwnd, L"NamespaceTreeControl"))
    {
        return true;
    }

    return HasDescendantWindowClass(hwnd, L"DirectUIHWND") &&
        HasDescendantWindowClass(hwnd, L"Breadcrumb Parent");
}

static bool IsForegroundInputSafeForCommit()
{
    HWND foreground = GetForegroundWindow();
    if (!foreground || IsShellFileDialogWindow(foreground))
    {
        return false;
    }

    DWORD foregroundProcessId = 0;
    DWORD foregroundThreadId = GetWindowThreadProcessId(foreground, &foregroundProcessId);
    if (foregroundThreadId == 0 || foregroundProcessId != GetCurrentProcessId())
    {
        return false;
    }

    GUITHREADINFO guiThreadInfo = { sizeof(GUITHREADINFO) };
    if (!GetGUIThreadInfo(foregroundThreadId, &guiThreadInfo))
    {
        return true;
    }

    HWND inputWindow = guiThreadInfo.hwndFocus ? guiThreadInfo.hwndFocus : guiThreadInfo.hwndCaret;
    if (!inputWindow)
    {
        return false;
    }

    DWORD inputProcessId = 0;
    if (!GetWindowThreadProcessId(inputWindow, &inputProcessId) || inputProcessId != foregroundProcessId)
    {
        return false;
    }

    HWND inputRoot = GetAncestor(inputWindow, GA_ROOT);
    return !IsShellFileDialogWindow(inputRoot ? inputRoot : foreground);
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
    auto* service = static_cast<UclTextService*>(param);
    service->AddRef();
    service->PipeLoop();
    service->Release();
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
    __try
    {
        return _owner ? _owner->InsertText(_context, ec, _text) : E_FAIL;
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
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

LRESULT CALLBACK UclTextService::WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp)
{
    __try
    {
        if (msg == WM_UCL_COMMIT)
        {
            auto* self = reinterpret_cast<UclTextService*>(GetWindowLongPtrW(hwnd, GWLP_USERDATA));
            auto* pText = reinterpret_cast<std::wstring*>(lp);
            if (pText)
            {
                __try
                {
                    if (self)
                    {
                        self->OnMessageCommit(*pText);
                    }
                }
                __finally
                {
                    delete pText;
                }
                return S_OK;
            }
            return E_FAIL;
        }
        if (msg == WM_NCCREATE)
        {
            auto* cs = reinterpret_cast<CREATESTRUCTW*>(lp);
            SetWindowLongPtrW(hwnd, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(cs->lpCreateParams));
        }
        return DefWindowProcW(hwnd, msg, wp, lp);
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return 0;
    }
}

void UclTextService::OnMessageCommit(const std::wstring& text)
{
    CommitText(text);
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

    if (IsBadHostProcess())
    {
        return S_OK;
    }

    // 建立隱藏視窗以利跨執行緒呼叫 (Marshalling)
    WNDCLASSEXW wc = { sizeof(WNDCLASSEXW) };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = g_hInst;
    wc.lpszClassName = L"UclTsfBridgeMsgWnd";
    RegisterClassExW(&wc);
    _msgHwnd = CreateWindowExW(0, wc.lpszClassName, nullptr, 0, 0, 0, 0, 0, HWND_MESSAGE, nullptr, g_hInst, this);

    g_pActiveService = this;
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
    UnadviseSinks();

    if (g_pActiveService == this)
    {
        g_pActiveService = nullptr;
    }

    StopPipeServer();

    if (_msgHwnd)
    {
        DestroyWindow(_msgHwnd);
        _msgHwnd = nullptr;
    }

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
    __try
    {
        if (!IsBadHostProcess())
        {
            UpdateFocusContext(docMgrFocus);
        }
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
    return S_OK;
}

STDMETHODIMP UclTextService::OnPushContext(ITfContext* context)
{
    __try
    {
        if (!IsBadHostProcess())
        {
            SetFocusContext(context);
        }
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
    return S_OK;
}

STDMETHODIMP UclTextService::OnPopContext(ITfContext*)
{
    __try
    {
        if (!IsBadHostProcess())
        {
            ITfDocumentMgr* docMgr = nullptr;
            if (_threadMgr && SUCCEEDED(_threadMgr->GetFocus(&docMgr)))
            {
                UpdateFocusContext(docMgr);
                docMgr->Release();
            }
        }
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
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

STDMETHODIMP UclTextService::OnSetFocus(BOOL foreground)
{
    __try
    {
        if (foreground && !IsBadHostProcess())
        {
            g_pActiveService = this;
        }
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
    return S_OK;
}

STDMETHODIMP UclTextService::OnTestKeyDown(ITfContext* context, WPARAM, LPARAM, BOOL* eaten)
{
    __try
    {
        if (!IsBadHostProcess())
        {
            SetFocusContext(context);
        }
        if (eaten) *eaten = FALSE;
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
    return S_OK;
}

STDMETHODIMP UclTextService::OnKeyDown(ITfContext* context, WPARAM, LPARAM, BOOL* eaten)
{
    __try
    {
        if (!IsBadHostProcess())
        {
            SetFocusContext(context);
        }
        if (eaten) *eaten = FALSE;
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
    return S_OK;
}

STDMETHODIMP UclTextService::OnTestKeyUp(ITfContext* context, WPARAM, LPARAM, BOOL* eaten)
{
    __try
    {
        if (!IsBadHostProcess())
        {
            SetFocusContext(context);
        }
        if (eaten) *eaten = FALSE;
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
    return S_OK;
}

STDMETHODIMP UclTextService::OnKeyUp(ITfContext* context, WPARAM, LPARAM, BOOL* eaten)
{
    __try
    {
        if (!IsBadHostProcess())
        {
            SetFocusContext(context);
        }
        if (eaten) *eaten = FALSE;
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {
        return E_FAIL;
    }
    return S_OK;
}

STDMETHODIMP UclTextService::OnPreservedKey(ITfContext*, REFGUID, BOOL* eaten)
{
    if (eaten) *eaten = FALSE;
    return S_OK;
}

bool UclTextService::HasContext()
{
    std::lock_guard<std::mutex> lock(_contextMutex);
    return _focusContext != nullptr;
}

HRESULT UclTextService::CommitText(const std::wstring& text)
{
    if (!IsForegroundInputSafeForCommit())
    {
        return E_ABORT;
    }

    if (!_threadMgr) return E_FAIL;
    
    ITfDocumentMgr* docMgr = nullptr;
    if (FAILED(_threadMgr->GetFocus(&docMgr)) || !docMgr)
    {
        return E_FAIL;
    }

    ITfContext* context = nullptr;
    if (FAILED(docMgr->GetTop(&context)) || !context)
    {
        docMgr->Release();
        return E_FAIL;
    }
    docMgr->Release();

    TfClientId clientId = _clientId;
    if (clientId == TF_CLIENTID_NULL)
    {
        context->Release();
        return E_ABORT;
    }

    auto* session = new (std::nothrow) UclEditSession(this, context, text);
    if (!session)
    {
        context->Release();
        return E_OUTOFMEMORY;
    }

    HRESULT sessionResult = E_FAIL;
    HRESULT hr = context->RequestEditSession(clientId, session, TF_ES_READWRITE | TF_ES_SYNC, &sessionResult);
    
    if (FAILED(hr))
    {
        HRESULT hrAsync = context->RequestEditSession(clientId, session, TF_ES_READWRITE, &sessionResult);
        if (SUCCEEDED(hrAsync))
            hr = S_OK;
    }
    
    session->Release();
    context->Release();
    
    return SUCCEEDED(hr) ? sessionResult : hr;
}

HRESULT UclTextService::InsertText(ITfContext* context, TfEditCookie ec, const std::wstring& text)
{
    if (!context)
    {
        return E_INVALIDARG;
    }

    // 嘗試方法 A: 使用標準 GetSelection -> SetText
    TF_SELECTION sel = {};
    ULONG fetched = 0;
    HRESULT hrA = context->GetSelection(ec, TF_DEFAULT_SELECTION, 1, &sel, &fetched);
    if (SUCCEEDED(hrA) && fetched > 0)
    {
        HRESULT hrSet = sel.range->SetText(ec, 0, text.c_str(), static_cast<LONG>(text.size()));
        if (SUCCEEDED(hrSet))
        {
            sel.range->Collapse(ec, TF_ANCHOR_END);
            context->SetSelection(ec, 1, &sel);
            sel.range->Release();
            return S_OK;
        }
        sel.range->Release();
    }

    // 嘗試方法 B: 使用 ITfInsertAtSelection
    ITfInsertAtSelection* insertAtSelection = nullptr;
    if (SUCCEEDED(context->QueryInterface(IID_ITfInsertAtSelection, reinterpret_cast<void**>(&insertAtSelection))))
    {
        HRESULT hrB = insertAtSelection->InsertTextAtSelection(
            ec,
            TF_IAS_NOQUERY,
            text.c_str(),
            static_cast<LONG>(text.size()),
            nullptr);
        insertAtSelection->Release();
        if (SUCCEEDED(hrB)) return S_OK;
    }

    return E_FAIL;
}

void UclTextService::StartPipeServer()
{
    if (IsBadHostProcess())
    {
        return;
    }

    std::lock_guard<std::mutex> lock(g_pipeMutex);
    if (g_hPipeThread) return;

    g_hPipeStopEvent = CreateEventW(nullptr, TRUE, FALSE, nullptr);
    if (!g_hPipeStopEvent) return;

    g_pPipeService = this;
    g_hPipeThread = CreateThread(nullptr, 0, PipeThreadProc, this, 0, &g_pipeThreadId);
    if (!g_hPipeThread)
    {
        CloseHandle(g_hPipeStopEvent);
        g_hPipeStopEvent = nullptr;
        g_pipeThreadId = 0;
        g_pPipeService = nullptr;
    }
}

void UclTextService::StopPipeServer()
{
    HANDLE thread = nullptr;
    HANDLE stopEvent = nullptr;
    DWORD threadId = 0;
    {
        std::lock_guard<std::mutex> lock(g_pipeMutex);
        if (g_pPipeService.load() != this || !g_hPipeThread || !g_hPipeStopEvent)
        {
            return;
        }
        thread = g_hPipeThread;
        stopEvent = g_hPipeStopEvent;
        threadId = g_pipeThreadId;
        SetEvent(stopEvent);
    }

    // Wake ConnectNamedPipe so the server can observe the stop event promptly.
    HANDLE pipe = CreateFileW(
        GetPipeNameForProcess(GetCurrentProcessId()).c_str(),
        GENERIC_READ | GENERIC_WRITE,
        0,
        nullptr,
        OPEN_EXISTING,
        0,
        nullptr);
    if (pipe != INVALID_HANDLE_VALUE)
    {
        CloseHandle(pipe);
    }

    if (thread && GetCurrentThreadId() != threadId)
    {
        // Keep this thread responsive while TSF/COM teardown is in progress.
        bool signaled = false;
        DWORD deadline = GetTickCount() + 1500;
        while (true)
        {
            DWORD now = GetTickCount();
            DWORD remaining = (now < deadline) ? (deadline - now) : 0;
            DWORD r = MsgWaitForMultipleObjects(1, &thread, FALSE, remaining, QS_SENDMESSAGE);
            if (r == WAIT_OBJECT_0)
            {
                signaled = true;
                break;
            }
            if (r == WAIT_OBJECT_0 + 1)
            {
                MSG msg;
                PeekMessageW(&msg, nullptr, 0, 0, PM_NOREMOVE);
                continue;
            }
            break; // WAIT_TIMEOUT or error
        }

        if (signaled)
        {
            std::lock_guard<std::mutex> lock(g_pipeMutex);
            if (thread == g_hPipeThread)
            {
                CloseHandle(g_hPipeThread);
                g_hPipeThread = nullptr;
            }
            if (stopEvent == g_hPipeStopEvent)
            {
                CloseHandle(g_hPipeStopEvent);
                g_hPipeStopEvent = nullptr;
            }
            g_pipeThreadId = 0;
            g_pPipeService = nullptr;
        }
    }
}

void UclTextService::PipeLoop()
{
    CoInitializeEx(nullptr, COINIT_MULTITHREADED);
    DWORD processId = GetCurrentProcessId();
    std::wstring pipeName = GetPipeNameForProcess(processId);

    while (g_hPipeStopEvent && WaitForSingleObject(g_hPipeStopEvent, 0) == WAIT_TIMEOUT)
    {
        HANDLE pipe = CreateNamedPipeW(
            pipeName.c_str(),
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            PIPE_UNLIMITED_INSTANCES, // 允許多個連線
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

        HRESULT hr = E_FAIL;
        HWND hwnd = _msgHwnd;
        if (g_pActiveService.load() == this && hwnd)
        {
            if (!IsForegroundInputSafeForCommit())
            {
                hr = E_ABORT;
            }
            else
            {
                auto* text = new (std::nothrow) std::wstring(Utf8ToWide(textUtf8));
                if (!text)
                {
                    hr = E_OUTOFMEMORY;
                }
                else if (PostMessageW(hwnd, WM_UCL_COMMIT, 0, reinterpret_cast<LPARAM>(text)))
                {
                    return "{\"ok\":true,\"queued\":true}\n";
                }
                else
                {
                    hr = HRESULT_FROM_WIN32(GetLastError());
                    delete text;
                }
            }
        }
        else
        {
            hr = E_ABORT; // 沒有活躍的服務
        }

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
