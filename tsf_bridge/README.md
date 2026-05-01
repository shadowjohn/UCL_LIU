# UCLLIU TSF Bridge Prototype

這是肥米輸入法的 TSF commit bridge 實驗版。

目標不是移植肥米輸入法，而是提供一個 Windows TSF Text Service，讓現有 Python `senddata()` 可以透過 named pipe 嘗試走 TSF commit。失敗時仍回到原本 `SendKeysCtypes` / 剪貼簿 / Big5 流程。

## Build

需要先安裝：

- Microsoft Visual Studio 2022 Build Tools 或 Visual Studio Community
- 「使用 C++ 的桌面開發」工作負載
- MSBuild
- MSVC C++ x64/x86 build tools
- Windows 10/11 SDK

在專案根目錄直接執行：

```bat
build_tsf.bat
```

這會編譯 `Release|x64`，成功後複製下列檔案到 `dist\tsf_bridge`：

```text
UclTsfBridge.dll
register_tsf_bridge.bat
unregister_tsf_bridge.bat
```

使用 Visual Studio Developer PowerShell：

```powershell
msbuild .\UclTsfBridge\UclTsfBridge.vcxproj /p:Configuration=Release /p:Platform=x64
```

目前專案使用本機 Visual Studio 18 的 `v145` toolset；如果要用 VS2022，將 `UclTsfBridge.vcxproj` 裡的 `PlatformToolset` 改成 `v143` 即可。

Release 使用 `/MT` 靜態連結 C/C++ runtime，降低使用者端需要額外安裝 VC Runtime 的機率。

## Register

```powershell
.\register_tsf_bridge.bat
```

註冊後到 Windows 輸入法清單切換 `UCLLIU TSF Bridge`。

## Pipe API

Pipe 名稱：

```text
\\.\pipe\uclliu_tsf_bridge
```

Request:

```json
{"cmd":"status"}
{"cmd":"commit_text","text":"肥"}
```

Response:

```json
{"ok":true,"active":true,"has_context":true}
{"ok":true}
{"ok":false,"error":"COMMIT_FAILED","hr":"0x8007139F"}
```

## 注意

- 第一版只驗證 commit bridge，不處理候選窗、不攔字根、不顯示 composition。
- Python 端必須保留原本 fallback，因為未切換到 TSF Bridge 或 context 消失時一定會失敗。
- 目前 DLL 用 HKCU `Software\Classes\CLSID` 做 per-user COM 註冊，通常不需要系統管理員權限。
