
Require:
	python-3.12.1.exe 【p3 目錄裡有，來自：https://www.python.org/ftp/python/3.12.1/python-3.12.1.exe 】
	無法使用 amd64，似乎無法正確出字，且用 amd64 編出的 exe 會被 windows defender 擋掉，x86 版可正常運作
	
	python.exe -m pip install --upgrade pip
	pip install pypiwin32==223
	pip install thread==0.1.3
	pip install pyaudio==0.2.14
	pip install setuptools==69.0.3
	
	swigwin 來自：https://www.swig.org/download.html
	環境變數 path: add UCL_LIU\python3\p3\swigwin-4.2.0
	
	pyWinhook 【p3 目錄裡有，來自：https://github.com/Tungsteno74/pyWinhook 】
	cd p3\pyWinhook
		python setup.py build
		python setup.py install
	pip install psutil==5.9.7
	pip install screeninfo==0.8.1
	pip install wxPython==4.2.1
	pip install pyinstaller==6.3.0
	
