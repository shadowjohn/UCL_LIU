
Require:
	python-3.12.1.exe 【p3 目錄裡有，來自：https://www.python.org/ftp/python/3.12.1/python-3.12.1.exe 】
	無法使用 amd64，似乎無法正確出字，且用 amd64 編出的 exe 會被 windows defender 擋掉，x86 版可正常運作

	環境變數 path: add C:\python312-32
	環境變數 path: add C:\python312-32\scripts

	
	python.exe -m pip install --upgrade pip
	pip install pypiwin32==223
	pip install thread==0.1.3
	pip install pyaudio==0.2.14
	pip install setuptools==69.0.3
	
	swigwin 來自：https://www.swig.org/download.html
	環境變數 path: add UCL_LIU\python3\p3\swigwin-4.2.0
	
	pyWinhook 【p3 目錄裡有，來自：https://github.com/Tungsteno74/pyWinhook 】
	還需安裝 visual studio 2022 且打開【使用 C++ 的桌面開發】

	
	手動編譯 pyWinhook
	執行「C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Visual Studio 2022\Visual Studio Tools\VC\x86 Native Tools Command Prompt for VS 2022」
	進到有「VS2022 的 Command Prompt」
	cd p3\pyWinhook
		python setup.py build
		python setup.py install

	或直接安裝
	pip install pyWinhook==1.6.2

	pip install psutil==5.9.7
	pip install screeninfo==0.8.1
	pip install wxPython==4.2.1
	pip install pyinstaller==6.3.0
	
