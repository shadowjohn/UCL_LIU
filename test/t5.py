# -*- coding: utf-8 -*-
import psutil
import win32com.client
import win32gui
import win32process

parr = {}
for proc in psutil.process_iter():
  #try:
  pinfo = proc.as_dict(attrs=['pid', 'name'])
  parr[pinfo['pid']]=pinfo['name']
  #except psutil.NoSuchProcess:
  #    pass
  #else:
  #    print(pinfo)
#print(parr)
hwnd = win32gui.GetForegroundWindow()
pid = win32process.GetWindowThreadProcessId(hwnd)
print hwnd
