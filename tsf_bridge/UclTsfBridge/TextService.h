#pragma once

#include "Globals.h"
#include <atomic>
#include <mutex>
#include <string>

class UclTextService;

class UclEditSession final : public ITfEditSession
{
public:
    UclEditSession(UclTextService* owner, ITfContext* context, const std::wstring& text);

    STDMETHODIMP QueryInterface(REFIID riid, void** ppvObject) override;
    STDMETHODIMP_(ULONG) AddRef() override;
    STDMETHODIMP_(ULONG) Release() override;
    STDMETHODIMP DoEditSession(TfEditCookie ec) override;

private:
    std::atomic<long> _refCount{ 1 };
    UclTextService* _owner = nullptr;
    ITfContext* _context = nullptr;
    std::wstring _text;
};

class UclTextService final :
    public ITfTextInputProcessor,
    public ITfThreadMgrEventSink,
    public ITfKeyEventSink
{
public:
    UclTextService();
    ~UclTextService();

    STDMETHODIMP QueryInterface(REFIID riid, void** ppvObject) override;
    STDMETHODIMP_(ULONG) AddRef() override;
    STDMETHODIMP_(ULONG) Release() override;

    STDMETHODIMP Activate(ITfThreadMgr* threadMgr, TfClientId clientId) override;
    STDMETHODIMP Deactivate() override;

    STDMETHODIMP OnInitDocumentMgr(ITfDocumentMgr* docMgr) override;
    STDMETHODIMP OnUninitDocumentMgr(ITfDocumentMgr* docMgr) override;
    STDMETHODIMP OnSetFocus(ITfDocumentMgr* docMgrFocus, ITfDocumentMgr* docMgrPrevFocus) override;
    STDMETHODIMP OnPushContext(ITfContext* context) override;
    STDMETHODIMP OnPopContext(ITfContext* context) override;

    STDMETHODIMP OnSetFocus(BOOL foreground) override;
    STDMETHODIMP OnTestKeyDown(ITfContext* context, WPARAM wParam, LPARAM lParam, BOOL* eaten) override;
    STDMETHODIMP OnKeyDown(ITfContext* context, WPARAM wParam, LPARAM lParam, BOOL* eaten) override;
    STDMETHODIMP OnTestKeyUp(ITfContext* context, WPARAM wParam, LPARAM lParam, BOOL* eaten) override;
    STDMETHODIMP OnKeyUp(ITfContext* context, WPARAM wParam, LPARAM lParam, BOOL* eaten) override;
    STDMETHODIMP OnPreservedKey(ITfContext* context, REFGUID rguid, BOOL* eaten) override;

    HRESULT CommitText(const std::wstring& text);
    HRESULT InsertText(ITfContext* context, TfEditCookie ec, const std::wstring& text);
    bool HasContext();
    void PipeLoop();

private:
    void AdviseSinks();
    void UnadviseSinks();
    void SetFocusContext(ITfContext* context);
    void UpdateFocusContext(ITfDocumentMgr* docMgr);
    void StartPipeServer();
    void StopPipeServer();
    std::string HandlePipeRequest(const std::string& request);

    static LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp);
    void OnMessageCommit(const std::wstring& text);

private:
    std::atomic<long> _refCount{ 1 };
    ITfThreadMgr* _threadMgr = nullptr;
    TfClientId _clientId = TF_CLIENTID_NULL;
    DWORD _threadMgrSinkCookie = TF_INVALID_COOKIE;
    bool _keySinkAdvised = false;
    ITfContext* _focusContext = nullptr;
    std::mutex _contextMutex;

    HANDLE _pipeThread = nullptr;
    HANDLE _pipeStopEvent = nullptr;
    HWND _msgHwnd = nullptr;
};

class UclClassFactory final : public IClassFactory
{
public:
    UclClassFactory();
    ~UclClassFactory();

    STDMETHODIMP QueryInterface(REFIID riid, void** ppvObject) override;
    STDMETHODIMP_(ULONG) AddRef() override;
    STDMETHODIMP_(ULONG) Release() override;
    STDMETHODIMP CreateInstance(IUnknown* outer, REFIID riid, void** ppvObject) override;
    STDMETHODIMP LockServer(BOOL lock) override;

private:
    std::atomic<long> _refCount{ 1 };
};
