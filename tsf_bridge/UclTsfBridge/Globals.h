#pragma once

#include <windows.h>
#include <msctf.h>

// UCLLIU TSF Bridge prototype GUIDs.
// 修改 GUID 會讓既有註冊失效；除非要建立另一個輸入法身分，否則不要改。
// {77B90778-7368-4F68-B022-C50005EBBE72}
inline const CLSID CLSID_UclTsfBridge =
{ 0x77b90778, 0x7368, 0x4f68, { 0xb0, 0x22, 0xc5, 0x00, 0x05, 0xeb, 0xbe, 0x72 } };

// {89F8BD7C-1B50-4F18-B44B-08E26900F030}
inline const GUID GUID_PROFILE_UclTsfBridge =
{ 0x89f8bd7c, 0x1b50, 0x4f18, { 0xb4, 0x4b, 0x08, 0xe2, 0x69, 0x00, 0xf0, 0x30 } };

constexpr wchar_t kServiceName[] = L"UCLLIU TSF Bridge";
constexpr wchar_t kPipeName[] = L"\\\\.\\pipe\\uclliu_tsf_bridge";

extern HINSTANCE g_hInst;
extern long g_dllRefCount;

void DllAddRef();
void DllRelease();
