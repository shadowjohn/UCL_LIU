# Chat History

## 2026-05-07

- 使用者回報 `Explorer.EXE` 很容易 crash。
- Windows 事件內容指出 faulting module 是 `D:\GD\UCL_LIU\dist\tsf_bridge\x64\UclTsfBridge.dll`，例外狀況代碼 `0xc0000005`，錯誤位移 `0x0000000000002c8c`。
- 初步方向：檢查 TSF bridge 的 C++ COM/TSF lifecycle、pipe thread 停止邏輯、hidden window `SendMessage` race、以及 DLL unload/Deactivate 行為。
- 已修正 `tsf_bridge/UclTsfBridge/TextService.cpp`：`Deactivate()` 會停止 pipe server、避免透過裸全域 active pointer 呼叫可能失效的 service、補上 hidden window message 參數檢查，並整理 pipe thread handle 生命週期。
- 已修正 `build_tsf.bat`：copy DLL 或 bat 失敗時會回報錯誤並停止，不再顯示誤導性的 `[OK]`。
- 建置 `Release|x64` 與 `Release|Win32` 皆成功且 0 warning/0 error。`dist\tsf_bridge\x64\UclTsfBridge.dll` 因被多個程序載入而無法覆蓋；新的 x64 DLL 在 `tsf_bridge\UclTsfBridge\x64\Release\UclTsfBridge.dll`。
- 使用者後續回報 `LINE.exe` crash，faulting module 仍是 `dist\tsf_bridge\x64\UclTsfBridge.dll`，錯誤位移仍是 `0x0000000000002c8c`，例外代碼 `0xc000041d`。判斷與 Explorer crash 是同一顆舊版 TSF DLL 的同一類問題。

## 2026-05-07（續）

- 使用者回報新的 `LINE.exe` crash：faulting module `dist\tsf_bridge\x64\UclTsfBridge.dll`，例外代碼 `0xc000041d`，錯誤**新位移** `0x0000000000002e9c`（比上次 `0x2c8c` 多約 0x210 bytes）。
- 觸發情境：LINE 開啟選檔對話框（IFileOpenDialog）時，於搜尋欄用 UCL LIU 輸入法打字出字。
- 根本原因分析：
  1. **主要**：file picker dialog 的 ITfContext 不支援 `TF_ES_READWRITE | TF_ES_SYNC`，`CommitText` 退回 async `TF_ES_READWRITE`。使用者選擇檔案後 dialog 關閉，TSF 釋放 context，但 async `DoEditSession` 仍被 dispatch → 存取已釋放的 context → AV → 例外從 COM callback 逃出 → `0xc000041d`。
  2. **次要**：`StopPipeServer` 用 `WaitForSingleObject`，若 pipe thread 同時在 `SendMessageW` 等 UI thread 抽訊息則死結。
- 已修正 `tsf_bridge/UclTsfBridge/TextService.cpp`：
  - `DoEditSession` 加 `__try/__except(EXCEPTION_EXECUTE_HANDLER)`（主要修正）
  - `WndProc` 加 `__try/__except(EXCEPTION_EXECUTE_HANDLER)`
  - `CommitText` async fallback 移除謊報的 `sessionResult = S_OK`
  - `StopPipeServer` 改用 `MsgWaitForMultipleObjects` + `PeekMessage` 迴圈（防止死結）
  - `Deactivate` 中 `DestroyWindow` 移到 `StopPipeServer` 之後（確保 pipe thread 停止後再摧毀視窗）
- 建置 Release|x64 與 Release|Win32 皆成功，0 warning / 0 error。新 DLL 在 `tsf_bridge\UclTsfBridge\x64\Release\UclTsfBridge.dll` 與 `Win32\Release\`。`dist\tsf_bridge\x64\UclTsfBridge.dll` 因被程序載入仍無法覆蓋，需關閉 LINE 後手動複製。

## 2026-05-07（再續）

- 使用者指出 TSF DLL 在 Explorer、檔案選擇對話框、Explorer 搜尋框/路徑欄等 shell TSF host 中，`pipe thread + SendMessageW + TF_ES_SYNC edit session` 仍有 crash/deadlock 風險。
- 已修正 `tsf_bridge/UclTsfBridge/TextService.cpp`：
  - 新增高風險 host process 排除：`explorer.exe`、`OpenWith.exe`、`PickerHost.exe`、`FilePicker.exe`、`FileOpenPicker.exe`、`SearchHost.exe`、`ShellExperienceHost.exe`、`StartMenuExperienceHost.exe` 不啟動 PipeServer。
  - 新增 foreground/input guard：commit 前確認前景視窗屬於目前 process，且不是 Explorer/file dialog shell window；LINE 內的 IFileOpenDialog 這類 `#32770` + shell child window 也會被擋下。
  - `commit_text` 從 `SendMessageW` 改為 `PostMessageW`，pipe thread 不再同步等待 TSF/UI thread；回應改為 `{"ok":true,"queued":true}`。
  - `WM_UCL_COMMIT` 改為接收 heap 配置的 `std::wstring*`，處理後釋放，實際 `CommitText()` 仍在 TSF thread 執行。
- 原樣建置因本機缺少專案指定的 `v145` toolset 失敗於 MSB8020；用命令列臨時覆寫 `/p:PlatformToolset=v143` 驗證 Release|x64 與 Release|Win32 皆成功，0 warning / 0 error。

## 2026-05-07（解除 DLL file lock）

- 使用者希望 unregister 後不用每次登出才能覆蓋 `UclTsfBridge.dll`。
- 已新增 `tsf_bridge\unlock_tsf_bridge.ps1` 與 `dist\tsf_bridge\unlock_tsf_bridge.ps1`：
  - 掃描目前載入 `UclTsfBridge.dll` 的程序，列出 process name / PID / module path。
  - 對非核心程序逐一詢問是否關閉；先嘗試 graceful close，必要時再二次詢問是否 force terminate。
  - `explorer.exe` 走確認後重啟 Explorer 的流程。
  - 核心程序、helper/regsvr32/uclliu/python 類程序會跳過，不主動終止。
- 已更新 `tsf_bridge\unregister_tsf_bridge.bat` 與 dist 版：
  - `regsvr32 /u` 會檢查錯誤碼。
  - unregister 成功後呼叫 `unlock_tsf_bridge.ps1`，協助釋放 file lock。
- 已更新 `build_tsf.bat`：會把 `unlock_tsf_bridge.ps1` 複製到 `dist\tsf_bridge`。
- 已更新 `uclliu.pyw`：
  - GUI unregister 改成同步執行 `regsvr32 /u /s`，能知道真正成敗。
  - unregister 成功後啟動 PowerShell helper，逐一處理鎖定 DLL 的程序。
  - `tsf_bridge_get_dll_path()` 會跳過 x86/Win32 DLL，避免 64-bit `regsvr32` 拿錯檔。
- 驗證：
  - PowerShell parser 檢查 source/dist helper 皆通過。
  - 本機沒有可用 Python 2 runtime，因此未能對 `uclliu.pyw` 做 Python 2 語法編譯檢查。
  - 目前仍載入舊 dist x64 DLL 的程序包含 `Code`、`explorer`、`LINE`、`msedgewebview2`、`Widgets`。

## 2026-05-07（修正 TSF build 工具鏈混版）

- 使用者回報 Win32 link 階段失敗：`LINK : fatal error LNK1101: MSPDB140.DLL 版本不正確`。
- 原因方向：`build_tsf.bat` 原本優先找 `%ProgramFiles%\Microsoft Visual Studio\18\Community\MSBuild...`，本機同時有 VS 18、VS 2022、VS 2019/2017 Build Tools，容易讓 MSBuild/toolset/PDB server 混版。
- 已更新 `build_tsf.bat`：
  - 移除 VS 18 優先路徑。
  - 優先使用 VS 2022，再 fallback VS 2019。
  - `vswhere` 搜尋限制為 `[16.0,18.0)`，避免抓到 VS 18。
  - 建置時覆寫 `/p:PlatformToolset=v143` 與 `/p:PreferredToolArchitecture=x64`，並加 `/nr:false`。
  - 建置前 `taskkill /IM mspdbsrv.exe /F`，避免舊 PDB server 造成 LNK1101。
- 驗證：使用 VS2022 MSBuild + `PlatformToolset=v143` 分別建置 `Release|Win32` 與 `Release|x64` 皆成功，0 warning / 0 error。

## 2026-05-07（build copy 時自動解除 DLL lock）

- 使用者回報 build 成功後 copy 到 `dist\tsf_bridge\x64\UclTsfBridge.dll` 失敗：檔案正由另一個程序使用。
- 已更新 `build_tsf.bat`：
  - 新增 `:CopyWithUnlock` subroutine。
  - x64/x86 DLL copy 第一次失敗時，會呼叫 `tsf_bridge\unlock_tsf_bridge.ps1`。
  - helper 會列出載入 `UclTsfBridge.dll` 的程序並逐一詢問是否關閉/重啟；完成後 build script 會自動 retry copy。
  - 若 retry 仍失敗，才停止並提示關閉剩餘程序後重跑。
- 未直接執行完整 `build_tsf.bat`，避免互動式 helper 在目前工作階段中關閉使用者的 Code/LINE/Explorer。
- 使用者執行 unregister 時遇到 `'""' is not recognized as an internal or external command`：
  - 原因是 `unregister_tsf_bridge.bat` 在 `if exist "%UNLOCK_SCRIPT%" (...)` 區塊內才設定 `PS_EXE`，但 `%PS_EXE%` 會在整個區塊解析前展開，導致命令變成空字串。
  - 已修正 source/dist 兩份 `unregister_tsf_bridge.bat`：將 `PS_EXE` 設定移到 `if` 區塊外。

## 2026-05-07（TSF 修正確認）

- 使用者回覆「看來可以了」，目前 TSF build / unregister / DLL lock 相關修正看起來已可接受。

## 2026-05-08（補上 VS 2026 TSF build）

- 使用者要求檢查 `.bat`，並加上 VS 2026 的編譯方式。
- 已更新 `build_tsf.bat`：
  - 優先偵測 VS 2026 / VS 18 的 MSBuild。
  - VS 2026 使用 `/p:PlatformToolset=v145`。
  - 找不到 VS 2026 時再 fallback 到 VS 2022/2019，維持 `/p:PlatformToolset=v143`。
  - `vswhere` 先掃 `[18.0,19.0)`，再掃舊的 `[16.0,18.0)`。
- 驗證：本機抓到 `C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\amd64\MSBuild.exe`，以 `v145` 成功建置 TSF Bridge Release x64/Win32，0 warning / 0 error。

## 2026-06-15（最近開發現況盤點）

- 目前 `master` / `origin/master` 停在 `531f967`、tag `v1.67`：新增 GitHub Actions 自動建置/發布流程，並更新 README release automation 說明。
- 近期核心開發脈絡仍是 TSF Bridge：修 Explorer/LINE/file picker crash、避免 shell host 中啟動 pipe server、改用 `PostMessageW` 排入 TSF thread commit、改善 unregister 後 DLL file lock 解除，以及 `build_tsf.bat` 的 VS 2026 / VS 18 `v145` 與 VS2022/2019 `v143` fallback。
- 工作區目前有未提交輸出檔：`dist\uclliu.exe`、`dist\tsf_bridge\x64\UclTsfBridge.dll`、`dist\tsf_bridge\x86\UclTsfBridge.dll`；`dist\pinyi.txt` 雖被 `git status` 標成 modified，但 blob hash 與 `HEAD` 相同，內容未變。
- 未追蹤檔包含 `.claude\settings.local.json`、`Web.config`、`dist\README.md`、`uclliu.zip`、`p27\PyInstaller-3.2.zip` 與解開的 `p27\PyInstaller-3.2\`。
- 潛在 CI 風險：`.github\workflows\build-and-release.yml` 會執行 `python p27\get-pip.py`，但 `p27\get-pip.py` 目前是未追蹤檔；若遠端 repo 沒有此檔，GitHub Actions 會在 bootstrap pip 階段失敗。

## 2026-06-15（修正 GitHub Actions release exe 啟動失敗）

- 使用者回報 GitHub Actions 發布的 `v1.67` release exe 啟動後跳出 `Fatal error detected: Failed to execute script uclliu`。
- 檢查 GitHub Actions run `27523920946`：job 顯示 success，但 log 中 `python p27\get-pip.py` 實際失敗，因 PowerShell 未 stop-on-error 被吞掉；PyInstaller 仍繼續產出 `dist\uclliu.exe`。
- 下載/檢查 release 產物：`uclliu.exe` 只有 5,463,548 bytes，且二進位字串可找到 `pyHook` / `win32api` / `pythoncom`，但找不到 `gtk` / `gobject` / `pango`；判斷 PyGTK 沒有進入 PyInstaller bundle。
- 根因：workflow 用 `msiexec /qn` 安裝 `pygtk-all-in-one-2.24.1.win32-py2.7.msi`，但 PyGTK all-in-one 在 quiet mode 會跳過 Python 自動偵測，必須指定 `TARGETDIR=C:\Python27`；原 workflow 也沒有檢查 MSI exit code 或 import 結果。
- 已更新 `.github\workflows\build-and-release.yml`：
  - Python / PyGTK MSI 安裝改用 `-PassThru` 檢查 exit code。
  - PyGTK 安裝指定 `TARGETDIR=C:\Python27`，並立即驗證 `import gtk, gobject, pango`。
  - 移除對未追蹤 `p27\get-pip.py` 的依賴，改用 `ensurepip` 與 repo 內的 `pip-20.3b1` wheel。
  - 依賴安裝後驗證 `gtk/gobject/pango/win32api/pythoncom/pyHook/pyaudio/psutil`。
  - 打包後檢查 exe 內含 `gtk/gobject/pango/pyHook/win32api/pythoncom` 字串，避免缺 PyGTK 的 exe 被發布。
- 已更新 `build.bat`：補上 `setlocal`、安全清理 build 目錄、TSF build / PyInstaller build / `dist\uclliu.exe` 產出檢查，避免 CI 繼續吞錯。
- 本機未完整重跑 build：目前本機沒有完整 `C:\Python27\python.exe`；已用 release exe 二進位檢查確認壞版缺 `gtk/gobject/pango`。

## 2026-06-15（GitHub Actions p27 依賴 SHA256 gate）

- 使用者決定走「SHA256 安全來源方案」，不在 CI 內重新從原始碼編譯所有 Python 2.7 legacy dependencies。
- 已新增 `p27\SHA256SUMS.txt`：只列 `.github\workflows\build-and-release.yml` 實際 release build 會用到的 14 個檔案。
- 已新增 `p27\verify_sha256.ps1`：
  - 預設驗證 `p27\SHA256SUMS.txt` 內的檔案。
  - 缺檔、hash 不合、manifest 格式錯誤、或路徑逃出 base directory 都會 fail。
- 已新增 `p27\test_verify_sha256.ps1`：用暫存檔測試 valid manifest pass、hash mismatch fail、missing file fail。
- 已新增 `p27\SOURCES.md`：記錄 release build gate 內每個 vendored dependency 的 expected source、workflow 用途，以及是否會執行 MSI/installer。
- 已更新 `.github\workflows\build-and-release.yml`：在 `Checkout repository` 後立即執行 `p27\verify_sha256.ps1`，所有 MSI/EXE/whl/tar/zip 被使用前先驗證 hash。
- 驗證：
  - `p27\test_verify_sha256.ps1` 先在 verifier 不存在時失敗，再完成實作後通過。
  - `p27\verify_sha256.ps1` 對目前 `p27` 內 14 個 release build dependency 全部通過。

## 2026-06-15（p27 原始收集檔來源複核）

- 使用者詢問原本收集的 MSI/EXE/whl/zip/tar/gz 是否安全。
- 已重新比對 release build gate 內檔案：
  - `python-2.7.13.msi` 對上 python.org 官方下載，且 Authenticode 簽章有效（Python Software Foundation）。
  - `pygtk-all-in-one-2.24.1.win32-py2.7.msi` 對上 GNOME 下載站；檔案本身未簽章。
  - `pywin32-221.win32-py2.7.exe` 對上 SourceForge pywin32 Build 221；檔案本身未簽章，但 workflow 只用 7-Zip 解包、不執行 installer。
  - `pyHook-1.5.1.win32-py2.7.exe` 對上 SourceForge pyHook 1.5.1；檔案本身未簽章，但 workflow 只用 7-Zip 解包、不執行 installer。
  - PyPI 發布物皆對上 PyPI JSON 內的 SHA256 digest。
- 已額外複核未納入 release build gate 的本機收集檔：
  - `get-pip.py` 對上 PyPA `get-pip` 固定 commit `049c52c665e8c5fd1751f942316e0a5c777d304f`。
  - `PyInstaller-3.2.zip`、`dis3-0.1.3-py2-none-any.whl`、`psutil-5.8.0-cp27-none-win32.whl`、`setuptools-44.1.1-py2.py3-none-any.whl` 對上 PyPI digest。
  - `VCForPython27.msi` Authenticode 簽章有效（Microsoft Corporation）。
- 判斷：原本收集的主要檔案來源可信度足夠；但未簽章的 legacy MSI/EXE 仍須維持固定 SHA256 gate，不應在 CI 內任意更新或改抓 latest。

## 2026-06-15（修正 GitHub Actions pyHook runtime 缺 DLL）

- Draft PR `#69` 觸發 GitHub Actions run `27525522152`。
- 已確認 checkout、`p27\verify_sha256.ps1`、MSBuild setup、Python 2.7 MSI、PyGTK MSI 都通過；新的 fail-fast 機制生效。
- 失敗點在 `Install pywin32 & pyHook` 的 import 驗證：7-Zip 解包 `pywin32` 與 `pyHook` 都成功，但 `python -c "import win32api, win32gui, pythoncom, pyHook"` 回報 `ImportError: DLL load failed: The specified module could not be found.`
- 本機以 `dumpbin /DEPENDENTS` 檢查 `p27\pyHook-1.5.1\build\lib.win32-2.7\pyHook\_cpyHook.pyd`，依賴：
  - `USER32.dll`
  - `python27.dll`
  - `MSVCR120.dll`
  - `KERNEL32.dll`
- 根因：GitHub `windows-2022` runner 沒有預裝 VS2013 x86 runtime 的 `MSVCR120.dll`，導致 `pyHook._cpyHook.pyd` 載入失敗。
- 已更新 workflow：
  - 在 PyGTK 後、pywin32/pyHook import 前，下載 Microsoft 官方 VS2013 x86 runtime `https://aka.ms/highdpimfc2013x86enu`。
  - 驗證 SHA256 `53b605d1100ab0a88b867447bbf9274b5938125024ba01f5105a9e178a3dcdbd` 與 Authenticode 簽章後才安裝。
  - 安裝後確認 `C:\Windows\SysWOW64\msvcr120.dll` 存在。
  - 將 `win32api`、`win32gui`、`pythoncom`、`pyHook` 改成逐一 import 驗證，之後失敗會更容易定位。

## 2026-06-15（修正 pywin32 postinstall 缺漏）

- GitHub Actions run `27525782043` 顯示 VS2013 runtime 安裝成功，但仍在 `Install pywin32 & pyHook` 失敗。
- 逐一 import 驗證指出第一個失敗的是 `win32api`，錯誤仍是 `ImportError: DLL load failed: The specified module could not be found.`
- 讀取 `pywin32-221.win32-py2.7.exe` 內部檔案後確認：
  - `PLATLIB\pywin32_system32\pywintypes27.dll`
  - `PLATLIB\pywin32_system32\pythoncom27.dll`
  - `SCRIPTS\pywin32_postinstall.py`
- 根因：workflow 只用 7-Zip 解包並 copy `PLATLIB` / `SCRIPTS`，但沒有執行 `pywin32_postinstall.py -install`；因此 `pywintypes27.dll` / `pythoncom27.dll` 沒被放到 Windows DLL 搜尋路徑，`win32api.pyd` 載入失敗。
- 已更新 workflow：copy `pywin32` 後執行 `C:\Python27\python.exe C:\Python27\Scripts\pywin32_postinstall.py -install`，失敗時立即中止。
- GitHub Actions run `27525931068` 已通過：
  - SHA256 gate、Python 2.7、PyGTK、VS2013 x86 runtime、pywin32/pyHook、pip dependencies、`build.bat`、packaged executable content check、artifact upload 全部成功。
  - `Publish GitHub Release` 在 PR run 中正確 skipped。
  - 下載 artifact 後確認 `uclliu.exe` 含 `gtk/gobject/pango/pyHook/win32api/pythoncom` 字串。
  - artifact 內 `uclliu.exe` SHA256：`D04D600555183F81B9ED0FF5D21501D40E3703BC6C57EB6466A1D0FDC1A660E7`。

## 2026-06-15（v1.68 發布前版本資訊更新）

- 使用者提醒正式發布 `v1.68` 前，程式碼版本 meta 也要同步更新。
- 已更新 `uclliu.pyw` 的 `VERSION` 為 `1.68`。
- 已更新 `metadata.txt` 的 `filevers`、`prodvers`、`FileVersion`、`ProductVersion` 為 `1.68`。
- 已更新 `README.md` 與 `CHANGELOG.md` 的 v1.68 release 說明。
- README 主下載連結改指向 `releases/download/v1.68` 的 Actions release asset，避免指到 `master/dist` 舊包。
