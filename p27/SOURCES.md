# Vendored Python 2.7 Dependency Sources

This directory contains legacy Windows build dependencies used by GitHub Actions.
The release workflow verifies the files listed in `SHA256SUMS.txt` before running
any MSI/EXE installer or extracting any archive.

To rotate a dependency:

1. Download it from the expected upstream source.
2. Verify the vendor/project page and file name manually.
3. Replace the file in `p27`.
4. Recompute SHA256 and update `SHA256SUMS.txt`.
5. Run `pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File p27\test_verify_sha256.ps1`.
6. Run `pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File p27\verify_sha256.ps1`.

## Release Build Gate

Only files in this table are used by `.github/workflows/build-and-release.yml`
and enforced by `SHA256SUMS.txt`.

| File | Expected source | Workflow use | Runs code |
| --- | --- | --- | --- |
| `python-2.7.13.msi` | `https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi` | Installs Python 2.7 x86 to `C:\Python27`. | Yes, MSI |
| `pygtk-all-in-one-2.24.1.win32-py2.7.msi` | `https://download.gnome.org/binaries/win32/pygtk/2.24/pygtk-all-in-one-2.24.1.win32-py2.7.msi` | Installs GTK/PyGTK/PyGObject/PyCairo into `C:\Python27`. | Yes, MSI |
| `pywin32-221.win32-py2.7.exe` | `https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win32-py2.7.exe/download` | Extracted with 7-Zip; `PLATLIB` and `SCRIPTS` are copied into `C:\Python27`, then `pywin32_postinstall.py -install` is run. | Python postinstall |
| `pyHook-1.5.1.win32-py2.7.exe` | `https://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/pyHook-1.5.1.win32-py2.7.exe/download` | Extracted with 7-Zip; `PLATLIB` is copied into `C:\Python27`. | No installer execution |
| `pip-20.3b1-py2.py3-none-any.whl` | PyPI `pip` 20.3 beta 1 | Installed with `python -m pip install --no-index`. | Python package install |
| `altgraph-0.17.4-py2.py3-none-any.whl` | PyPI `altgraph` 0.17.4 | Installed with `python -m pip install --no-index`. | Python package install |
| `macholib-1.16.3-py2.py3-none-any.whl` | PyPI `macholib` 1.16.3 | Installed with `python -m pip install --no-index`. | Python package install |
| `configparser-4.0.2-py2.py3-none-any.whl` | PyPI `configparser` 4.0.2 | Installed with `python -m pip install --no-index`. | Python package install |
| `future-0.18.0-cp27-none-any.whl` | PyPI `future` 0.18.0 | Installed with `python -m pip install --no-index`. | Python package install |
| `psutil-6.1.1-cp27-none-win32.whl` | PyPI `psutil` 6.1.1 | Installed with `python -m pip install --no-index`. | Python package install |
| `PyAudio-0.2.11-cp27-cp27m-win32.whl` | PyPI `PyAudio` 0.2.11 | Installed with `python -m pip install --no-index`. | Python package install |
| `pywin32_ctypes-0.2.0-py2.py3-none-any.whl` | PyPI `pywin32-ctypes` 0.2.0 | Installed with `python -m pip install --no-index`. | Python package install |
| `pefile-2017.8.1.zip` | PyPI `pefile` 2017.8.1 source archive | Extracted with 7-Zip, then installed with `python setup.py install`. | Python setup install |
| `PyInstaller-3.4.tar.gz` | PyPI `PyInstaller` 3.4 source archive | Extracted with tar, then installed with `python setup.py install`. | Python setup install |

## CI-Downloaded Runtime

The workflow downloads this Microsoft runtime at build time instead of vendoring
it in `p27`. The workflow pins the expected SHA256 before running the installer
and also verifies the Authenticode signature.

| File | Expected source | SHA256 | Workflow use |
| --- | --- | --- | --- |
| `vcredist2013-x86.exe` | `https://aka.ms/highdpimfc2013x86enu` | `53b605d1100ab0a88b867447bbf9274b5938125024ba01f5105a9e178a3dcdbd` | Installs the VC++ 2013 x86 runtime required by `pyHook._cpyHook.pyd` (`MSVCR120.dll`). |

## Not Part Of The Release Build Gate

The workflow does not currently use these files, so they are intentionally not
listed in `SHA256SUMS.txt`:

- `get-pip.py`: matches PyPA `get-pip` commit `049c52c665e8c5fd1751f942316e0a5c777d304f`.
- `PyInstaller-3.2.zip`: matches PyPI `PyInstaller` 3.2.
- `dis3-0.1.3-py2-none-any.whl`: matches PyPI `dis3` 0.1.3.
- `psutil-5.8.0-cp27-none-win32.whl`: matches PyPI `psutil` 5.8.0.
- `setuptools-44.1.1-py2.py3-none-any.whl`: matches PyPI `setuptools` 44.1.1.
- `VCForPython27.msi`: has a valid Microsoft Authenticode signature.
- unpacked source/build helper directories under `p27`
