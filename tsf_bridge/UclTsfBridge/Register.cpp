#include "Globals.h"
#include <strsafe.h>

static HRESULT GetModulePath(wchar_t* path, DWORD chars)
{
    DWORD copied = GetModuleFileNameW(g_hInst, path, chars);
    return copied > 0 && copied < chars ? S_OK : HRESULT_FROM_WIN32(GetLastError());
}

static HRESULT SetRegString(HKEY root, const wchar_t* subKey, const wchar_t* name, const wchar_t* value)
{
    HKEY key = nullptr;
    LONG rc = RegCreateKeyExW(root, subKey, 0, nullptr, 0, KEY_WRITE, nullptr, &key, nullptr);
    if (rc != ERROR_SUCCESS)
    {
        return HRESULT_FROM_WIN32(rc);
    }

    rc = RegSetValueExW(
        key,
        name,
        0,
        REG_SZ,
        reinterpret_cast<const BYTE*>(value),
        static_cast<DWORD>((wcslen(value) + 1) * sizeof(wchar_t)));
    RegCloseKey(key);
    return HRESULT_FROM_WIN32(rc);
}

static HRESULT RegisterComServer()
{
    wchar_t clsidText[64] = {};
    StringFromGUID2(CLSID_UclTsfBridge, clsidText, ARRAYSIZE(clsidText));

    wchar_t modulePath[MAX_PATH] = {};
    HRESULT hr = GetModulePath(modulePath, ARRAYSIZE(modulePath));
    if (FAILED(hr))
    {
        return hr;
    }

    wchar_t clsidKey[256] = {};
    StringCchPrintfW(clsidKey, ARRAYSIZE(clsidKey), L"Software\\Classes\\CLSID\\%s", clsidText);
    hr = SetRegString(HKEY_CURRENT_USER, clsidKey, nullptr, kServiceName);
    if (FAILED(hr))
    {
        return hr;
    }

    wchar_t inprocKey[300] = {};
    StringCchPrintfW(inprocKey, ARRAYSIZE(inprocKey), L"%s\\InProcServer32", clsidKey);
    hr = SetRegString(HKEY_CURRENT_USER, inprocKey, nullptr, modulePath);
    if (FAILED(hr))
    {
        return hr;
    }
    hr = SetRegString(HKEY_CURRENT_USER, inprocKey, L"ThreadingModel", L"Apartment");
    if (FAILED(hr))
    {
        return hr;
    }
    return S_OK;
}

static void DeleteRegTree(HKEY root, const wchar_t* subKey)
{
    RegDeleteTreeW(root, subKey);
}

static HRESULT RegisterTextService()
{
    ITfInputProcessorProfiles* profiles = nullptr;
    HRESULT hr = CoCreateInstance(
        CLSID_TF_InputProcessorProfiles,
        nullptr,
        CLSCTX_INPROC_SERVER,
        IID_ITfInputProcessorProfiles,
        reinterpret_cast<void**>(&profiles));
    if (FAILED(hr))
    {
        return hr;
    }

    hr = profiles->Register(CLSID_UclTsfBridge);
    if (SUCCEEDED(hr))
    {
        hr = profiles->AddLanguageProfile(
            CLSID_UclTsfBridge,
            MAKELANGID(LANG_CHINESE, SUBLANG_CHINESE_TRADITIONAL),
            GUID_PROFILE_UclTsfBridge,
            const_cast<WCHAR*>(kServiceName),
            static_cast<ULONG>(wcslen(kServiceName)),
            nullptr,
            0,
            0);
    }
    profiles->Release();
    if (FAILED(hr))
    {
        return hr;
    }

    ITfCategoryMgr* categoryMgr = nullptr;
    hr = CoCreateInstance(
        CLSID_TF_CategoryMgr,
        nullptr,
        CLSCTX_INPROC_SERVER,
        IID_ITfCategoryMgr,
        reinterpret_cast<void**>(&categoryMgr));
    if (SUCCEEDED(hr))
    {
        hr = categoryMgr->RegisterCategory(
            CLSID_UclTsfBridge,
            GUID_TFCAT_TIP_KEYBOARD,
            CLSID_UclTsfBridge);
        categoryMgr->Release();
    }
    return hr;
}

static void UnregisterTextService()
{
    ITfInputProcessorProfiles* profiles = nullptr;
    HRESULT hr = CoCreateInstance(
        CLSID_TF_InputProcessorProfiles,
        nullptr,
        CLSCTX_INPROC_SERVER,
        IID_ITfInputProcessorProfiles,
        reinterpret_cast<void**>(&profiles));
    if (SUCCEEDED(hr))
    {
        profiles->RemoveLanguageProfile(
            CLSID_UclTsfBridge,
            MAKELANGID(LANG_CHINESE, SUBLANG_CHINESE_TRADITIONAL),
            GUID_PROFILE_UclTsfBridge);
        profiles->Unregister(CLSID_UclTsfBridge);
        profiles->Release();
    }

    ITfCategoryMgr* categoryMgr = nullptr;
    hr = CoCreateInstance(
        CLSID_TF_CategoryMgr,
        nullptr,
        CLSCTX_INPROC_SERVER,
        IID_ITfCategoryMgr,
        reinterpret_cast<void**>(&categoryMgr));
    if (SUCCEEDED(hr))
    {
        categoryMgr->UnregisterCategory(
            CLSID_UclTsfBridge,
            GUID_TFCAT_TIP_KEYBOARD,
            CLSID_UclTsfBridge);
        categoryMgr->Release();
    }
}

STDAPI DllRegisterServer()
{
    HRESULT hrInit = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);
    HRESULT hr = RegisterComServer();
    if (SUCCEEDED(hr))
    {
        hr = RegisterTextService();
    }
    if (SUCCEEDED(hrInit))
    {
        CoUninitialize();
    }
    return hr;
}

STDAPI DllUnregisterServer()
{
    HRESULT hrInit = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);
    UnregisterTextService();

    wchar_t clsidText[64] = {};
    StringFromGUID2(CLSID_UclTsfBridge, clsidText, ARRAYSIZE(clsidText));
    wchar_t clsidKey[256] = {};
    StringCchPrintfW(clsidKey, ARRAYSIZE(clsidKey), L"Software\\Classes\\CLSID\\%s", clsidText);
    DeleteRegTree(HKEY_CURRENT_USER, clsidKey);

    if (SUCCEEDED(hrInit))
    {
        CoUninitialize();
    }
    return S_OK;
}
