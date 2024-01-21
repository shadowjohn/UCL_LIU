# -*- coding: utf-8 -*-
VERSION = "3.01"

# Debug 模式
is_DEBUG_mode = True
import os
#os.environ['PYTHONIOENCODING'] = 'utf-8'
#os.environ['PYTHONUTF8'] = '1'
import portalocker
# Force 950 fix utf8-beta cp65001
# should fix before import configparser
#chcp_cmd = "C:\\Windows\\System32\\chcp.com"
#if my.is_file(chcp_cmd) == True:
#  my.system(chcp_cmd + " 950");
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
#import gtk
#from gtk import gdk 
    
#import gobject
import hashlib
import php
my = php.kit()
# trad to simp or simp to trad
import stts 
import re
#import win32api
# 2022-08-09 參考 https://stackoverflow.com/questions/4357258/how-to-get-the-height-of-windows-taskbar-using-python-pyqt-win32
# 可以取得工作列高度
from win32api import GetMonitorInfo, MonitorFromPoint


import configparser
#,,,z ,,,x 用thread去輸出字
import thread
import base64
import random
# 播放打字音用
import pyaudio
#import audioop
import wave

from screeninfo import get_monitors

#2021-08-08 新版右下角 traybar
from traybar import SysTrayIcon

paudio_player = None
#2021-10-28 同時間只能一個執行緒播放
is_sound_playing = False
sound_playing_s = ""

PWD = os.path.dirname(os.path.realpath(sys.argv[0]))

import clip

import wx

#if "a" in []:
#	#print("TEST")
#sys.exit(0)

#paudio_player = pyaudio.PyAudio()
# 播放打字音用
#from pydub import AudioSegment
#from pydub.playback import play

# 2022-12-02
# 強制使用 CP950 CHCP CP950
# From : https://stackoverflow.com/questions/55899664/is-there-a-way-to-change-the-console-code-page-from-within-python
# 似乎沒啥用
#os.system("chcp 950");
#import locale
#LOCALE_ENCODING = locale.getpreferredencoding()
#print("LOCALE_ENCODING: %s" % (LOCALE_ENCODING))
# 改用 i18n
import myi18n
my18 = myi18n.kit()
#print my18.auto('test')
#sys.exit()

# Fix exit crash problem
# 改用 
# https://stackoverflow.com/questions/23727539/runtime-error-in-python/24035224#24035224
# 用來取反白字
# https://stackoverflow.com/questions/1007185/how-to-retrieve-the-selected-text-from-the-active-window
# import win32ui
# https://superuser.com/questions/1120624/run-script-on-any-selected-text

# 額外出字處理的 app
f_arr = [ "putty","pietty","pcman","xyplorer","kinza.exe","oxygennotincluded.exe","iedit.exe","iedit_.exe","rimworldwin64.exe" ]
f_big5_arr = [ "zip32w","daqkingcon.exe","EWinner.exe" ]
# 不使用肥米的 app
# 2021-03-19 2077 也不能使用肥米
# 2021-07-03 vncviewer.exe 不需要肥米
f_pass_app = [ "mstsc.exe","cyberpunk2077.exe","vncviewer.exe" ]

# 2019-10-20 增加出字模式
# 這是右下角 肥 的 icon
UCL_PIC_BASE64 = "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAACUWAAAlFgAAAAAAAAAAAAD/////+Pf4//n6+//8+/n/4ebh/+3y8f////////////n69v/u9Ov/6u7o/+ru6P/q7+n/8vjy//7+////////+vTu/5W0e/+w1cv/1Na0/1mxPP9mvWL/0+bm/+fk0/+BwmD/YsVI/16+Rv9evkb/X8BG/2jGWP+01cX///////bu5v9wq0D/cbmQ/9jhyf+h1oP/Rq4t/5LAuv+xtIf/Qagu/4fMg/+d3I7/m9uO/5zXif9juzf/Vatp/+ny+f///f3/nbFt/1OoZP/t9v3/7O3Y/1StOf+LvbT/pKd5/06sU//i7ff/////////////////p7Z7/0WnSP/U5e3//////7/MkP9NqE7/2+Tv/+vt2P9Trjn/jL21/6Wnef9OrFP/4+73/////////////////8bCnv9kqmD/0uPo///////MyKr/Q4k1/22cbf+uza7/VK47/4y9tf+lp3n/TqxT/+Pu9//////////////////18e3/7fDv//7+////////zsKu/0WbKP9HqTD/TLM7/0CqMP+NvbX/pad5/06sVP/j7vf//////////////////////////////////////87Crf9IoTX/m76j/2auOv81sCT/jb22/6Wne/9FrzT/iNKC/5faiP+X2of/ldmG/5TWiv/G3NT////////////Owq3/R6Az/7zh2v/H0Kj/Ragr/4y9tf+mp3z/QK8l/1y6Rf9IsCT/QrUw/165Qv9AriH/jbap////////////zsKt/0miNv+St5X/erBj/0iqM/+MvbX/pad6/02rUP/S1tn/cZRC/1yydv/g2tH/Zacx/4u4qf///////////87Crv9InS7/VZtD/0edPf9EpjT/jL21/6Wnef9PrVT/3uDo/3SVRf9guHz/7+ff/2mqM/+Lt6n////////////Owq7/R50o/1WkTf+Gsoz/VK48/4y9tf+lp3n/T61U/97g6P90lUX/YLd8/+/n3/9pqjP/i7ep////////////zsKt/0egM/+z1tD/4uHR/1StOf+MvbX/pad6/06tUv/X3eD/cpZE/122ef/n49f/Z6oy/4u3qf///////////87Crf9CnSP/Yaha/3SlVf89pCf/jLy0/6Sne/8/sCb/ZMVQ/0qyKP9EujX/aMVN/0SxIv+Mtqn////////////b0MX/dppZ/2+mVv9uplb/bJ9d/67Jyf/LyrX/icJ2/4jId/+KyXn/ish5/4jId/+Hw3v/vtDO/////////////f39//n1+P/59Pf/+fT3//n1+P/8/P3///7///77/v/++/7//vv+//77/v/++/7//vv+///+////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
ICON_PATH = PWD + "\\icon.ico"
DEFAULT_OUTPUT_TYPE = "DEFAULT"
#BIG5
#PASTE

#import pywinauto             
#pwa = pywinauto.keyboard



# 2021-08-08 將簡、繁轉換抽離成獨立 class
mystts = stts.kit()


#2022-09-02 改用 opencc 簡繁轉換
# 嘗試修正 ,,,z 在轉 簡字回字碼，有些語句如 「小当家->小當傢，天后->天後」這種問題
from opencc import OpenCC
myopencc = OpenCC('s2t')





message = ("\nUCLLIU 肥米輸入法\nBy 羽山秋人(https://3wa.tw)\nBy Benson9954029 (https://github.com/Benson9954029)\nVersion: %s\n\n若要使用 Debug 模式：uclliu.exe -d\n" % (VERSION));

def about_uclliu():
  _msg_text = ("肥米輸入法\n\n作者：羽山秋人 (https://3wa.tw)\n作者：Benson9954029 (https://github.com/Benson9954029)\n版本：%s" % VERSION)
  _msg_text += "\n\n熱鍵提示：\n\n"
  _msg_text += "「,,,VERSION」目前版本\n"
  _msg_text += "「'ucl」同音字查詢\n"
  _msg_text += "「';zo6」注音查詢\n"
  _msg_text += "「,,,UNLOCK」回到正常模式\n"
  _msg_text += "「,,,LOCK」進入遊戲模式\n"
  _msg_text += "「,,,C」簡體模式\n"
  _msg_text += "「,,,T」繁體模式\n"
  _msg_text += "「,,,S」UI變窄\n"
  _msg_text += "「,,,L」UI變寬\n"
  _msg_text += "「,,,+」UI變大\n"
  _msg_text += "「,,,-」UI變小\n"
  _msg_text += "「,,,X」框字的字根轉回文字\n"
  _msg_text += "「,,,Z」框字的文字變成字根\n"
  return _msg_text  

if len(sys.argv)!=2:
  print( my.utf8tobig5(message) );
elif sys.argv[1]=="-d":
  is_DEBUG_mode = True

def debug_print(data):
  global is_DEBUG_mode
  if is_DEBUG_mode == True:
    try:
      print(data)
    except:
      pass

#debug_print("sys.argv[1]: ")
#debug_print(sys.argv[1])
#my.exit()
    
def md5_file(fileName):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        debug_print("Reading file has problem:", filename)
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest()


#PWD=my.pwd()   
#my.file_put_contents("c:\\temp\\aaa.txt",PWD);
#debug_print(PWD)
#sys.exit(0)


app = wx.App(False)
#win.set_modal(True)
#win.set_resizable(False)
win = wx.Frame(None, wx.ID_ANY, "Hello, UCL_LIU!")
# 將窗口設置爲自動佈局(自動展開)
win.SetAutoLayout(True)

#此是防止重覆執行
#if os.path.isdir("C:\\temp") == False:
#  os.mkdir("C:\\temp")
import ctypes


check_file_run = open(PWD + '\\UCLLIU.lock', "a+")
try:  
  portalocker.lock(check_file_run, portalocker.LOCK_EX | portalocker.LOCK_NB)
except:
  #md = gtk.MessageDialog(None, 
  #        gtk.DIALOG_DESTROY_WITH_PARENT, 
  #        gtk.MESSAGE_QUESTION, 
  #        gtk.BUTTONS_OK, "【肥米輸入法】已執行...")          
  #md.set_position(gtk.WIN_POS_CENTER)
  dlg = wx.MessageDialog(win, "【肥米輸入法】已執行...", "肥米輸入法", wx.OK)
  result = dlg.ShowModal()
  #dlg.Destroy()
  #response = md.run()            
  #if response == gtk.RESPONSE_OK or response == gtk.RESPONSE_DELETE_EVENT:
  if result == wx.ID_OK:
    print("OK button pressed")
    #md.destroy()
    dlg.Destroy()
    ctypes.windll.user32.PostQuitMessage(0)
    #FlagStopUpdateGUI = True
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    sys.exit(0)
         

import pythoncom, pyWinhook
from pyWinhook import HookManager
from pyWinhook.HookManager import HookConstants 

import win32clipboard
import SendKeysCtypes
import time

#http://wiki.alarmchang.com/index.php?title=Python_%E5%AD%98%E5%8F%96_Windows_%E7%9A%84%E5%89%AA%E8%B2%BC%E7%B0%BF_ClipBoard_%E7%AF%84%E4%BE%8B
import win32gui
import win32process
import psutil
#import win32com
import win32con
#import win32com.client


#2023-03-29 判斷作業系統版本
# Issue 177、Win11 裡的 notepad 如果不改字型為 MingLiu 無法正常出字，改成強制複製貼上修正
#debug_print(platform.version());
#sys.exit(0)

import platform
os_version = platform.release()

def isWin11():
  # From : https://stackoverflow.com/questions/68899983/get-current-windows-11-release-in-python
  # From : https://www.digitalocean.com/community/tutorials/python-system-command-os-subprocess-call
  # From : https://stackoverflow.com/questions/68899983/get-current-windows-11-release-in-python  這個可以
  #if sys.getwindowsversion().build > 20000:
  # 失敗
  data = ""
  wmic_cmd = "C:\\Windows\\System32\\wbem\\WMIC.exe"
  if my.is_file(wmic_cmd) == False:
    # windows 11 沙箱，沒有 WMIC 這個指令
    # issue 184、windows 沙箱在 1.55 版以後無法使用，發現是沙箱缺少 wmic.exe 指令
    version = platform.version()
    if 'Windows 7' in version:
        return False
    elif 'Windows 8' in version:
        return False
    elif 'Windows 10' in version:
        return False
    elif 'Windows 8.1' in version:
        return False
    else:
        # python 2.7 platform 讀不到版號!?
        return True
  try:
    data = my.system("%s os get name" % (wmic_cmd));
  except e:
    debug_print(e)
  #debug_print("GGG %s" % (data))
  if my.is_string_like(str(data),"Windows 11"):
    return True
  else:
    return False

if isWin11():
  os_version = "11"
#sys.exit()  
# 在此可以確定使用者是 win7 win10 win11  
# os_version 7 8 10 11
debug_print("os_version: %s" % (os_version))
#debug_print("sys.getwindowsversion().build: %s" % (sys.getwindowsversion().build))


#2023-03-10 在肥米啟動後，將優先性「priority」設為高，避免有些暫用cpu高的程式啟動後，肥米打字會卡
#參考:https://stackoverflow.com/questions/1023038/change-process-priority-in-python-cross-platform
p = psutil.Process(os.getpid())
#print("nice: %s" % (p.nice())) # default 32
#p.nice(psutil.HIGH_PRIORITY_CLASS) # 這樣會變 128
p.nice(256)
#print("nice: %s" % (p.nice()))

#2018-07-13 1.12版增加
#檢查 C:\temp\UCLLIU.ini 初始化設定檔
#取螢幕大小

#2019-03-02 調整，將 UCLLIU.ini 跟隨在 UCLLIU.exe 旁
INI_CONFIG_FILE = 'C:\\temp\\UCLLIU.ini'
if my.is_file(INI_CONFIG_FILE):
  my.copy(INI_CONFIG_FILE,PWD+"\\UCLLIU.ini")
  my.unlink(INI_CONFIG_FILE)
INI_CONFIG_FILE = PWD + "\\UCLLIU.ini" 

#user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()

#screen_width=user32.GetSystemMetrics(0)
#screen_height=user32.GetSystemMetrics(1)
#debug_print("screen width, height : %s , %s" % (screen_width,screen_height))
#window = gtk.Window()
#From : https://www.familylifemag.com/question/701406/how-do-i-get-monitor-resolution-in-python
monitors = get_monitors()
myScreenStatus = {
  "main_monitor" : 0, # 面積大的當作 main
  "first_time_x": 0, # 系統初始位置，使用下面主螢幕中心點位置移至右下150x150
  "first_time_y": 0,
  "screens": [
    # x,y,w,h,area, c_x,c_y
  ]
}
debug_print("get_n_monitors(): %d\n" % (len(monitors)));
#print(my.json_encode(myopencc.convert(u"所以我说那个酱汁呢，小当家你是在...")))
#debug_print(myScreensObj.get_monitor_geometry(0)); #gtk.gdk.Rectangle(1280, 0, 2560, 1080)
#debug_print(myScreensObj.get_monitor_geometry(1)); #gtk.gdk.Rectangle(0, 59, 1280, 1024)

#for i in range(0,myScreensObj.get_n_monitors()):
for i, monitor in enumerate(monitors, 1):
  d = {
    "x": monitor.x,
    "y": monitor.y,
    "w": monitor.width,
    "h": monitor.height,
    "area": (monitor.width * monitor.height),
    "c_x": (monitor.x + (monitor.width / 2)),
    "c_y": (monitor.y + (monitor.height / 2))
  }
  myScreenStatus["screens"].append(d);
  if i == 0:
    myScreenStatus["main_monitor"] = i;
    #調整第一次執行的中心位置
    myScreenStatus["first_time_x"] = d["c_x"]+150
    myScreenStatus["first_time_y"] = d["c_y"]+150    
  else:
    _is_bigger = True
    for j in range(0,len(myScreenStatus["screens"])-1):
      if myScreenStatus["screens"][j] > d["area"]:
        _is_bigger = False;
        break;
    if _is_bigger == True:
      myScreenStatus["main_monitor"]=i; # 最大螢幕易主
      myScreenStatus["first_time_x"] = d["c_x"]+150
      myScreenStatus["first_time_y"] = d["c_y"]+150
      
debug_print(my.json_encode(myScreenStatus));
#screen_width = gtk.gdk.screen_width()
#screen_height = gtk.gdk.screen_height()

#debug_print("screen_width: %d\n" % (screen_width));
#debug_print("screen_height: %d\n" % (screen_height));
  
config = configparser.ConfigParser()
config['DEFAULT'] = {
                      "X": myScreenStatus["first_time_x"],
                      "Y": myScreenStatus["first_time_y"],
                      "ALPHA": "1", #嘸蝦米全顯示時時的初值
                      "NON_UCL_ALPHA": "0.2", #英數時的透明度
                      "SHORT_MODE": "0", #0:簡短畫面，或1:長畫面
                      "ZOOM": "1", #整體比例大小
                      "SEND_KIND_1_PASTE": "", #出字模式1
                      "SEND_KIND_2_BIG5": "", #出字模式2
                      "SEND_KIND_3_NOUCL":"", #Force no UCL
                      "KEYBOARD_VOLUME": "30", #打字聲音量，0~100
                      "SP": "0", #短根
                      "SHOW_PHONE_CODE": "0", #顯示注音讀音
                      "CTRL_SP": "0", #使用CTRL+SPACE換肥米
                      "PLAY_SOUND_ENABLE": "0", #打字音
                      "STARTUP_DEFAULT_UCL": "1", #啟動時，預設為 肥，改為 0 則為 英
                      "ENABLE_HALF_FULL": "1" #允許切換 全形半形
                    };
if my.is_file(INI_CONFIG_FILE):
  _config = configparser.ConfigParser()
  _config.read(INI_CONFIG_FILE, encoding='utf-8')    
  for k in _config['DEFAULT'].keys(): # ['X','Y','ALPHA','ZOOM','SHORT_MODE','SEND_KIND_1_PASTE','SEND_KIND_2_BIG5'] 
    if k in config['DEFAULT'].keys():
      config['DEFAULT'][k]=_config['DEFAULT'][k]
      
config['DEFAULT']['X'] = str(int(float(config['DEFAULT']['X'])));
config['DEFAULT']['Y'] = str(int(float(config['DEFAULT']['Y']))); 
config['DEFAULT']['ALPHA'] = "%.1f" % ( float(config['DEFAULT']['ALPHA'] ));
config['DEFAULT']['NON_UCL_ALPHA'] = "%.1f" % ( float(config['DEFAULT']['NON_UCL_ALPHA'] ));
config['DEFAULT']['SHORT_MODE'] = str(int(config['DEFAULT']['SHORT_MODE']));
config['DEFAULT']['ZOOM'] = "%.2f" % ( float(config['DEFAULT']['ZOOM'] ));
config['DEFAULT']['SEND_KIND_1_PASTE'] = str(config['DEFAULT']['SEND_KIND_1_PASTE']);
config['DEFAULT']['SEND_KIND_2_BIG5'] = str(config['DEFAULT']['SEND_KIND_2_BIG5']);
config['DEFAULT']['KEYBOARD_VOLUME'] = str(int(config['DEFAULT']['KEYBOARD_VOLUME']));
config['DEFAULT']['SP'] = str(int(config['DEFAULT']['SP']));
config['DEFAULT']['SHOW_PHONE_CODE'] = str(int(config['DEFAULT']['SHOW_PHONE_CODE']));
config['DEFAULT']['CTRL_SP'] = str(int(config['DEFAULT']['CTRL_SP']));
config['DEFAULT']['PLAY_SOUND_ENABLE'] = str(int(config['DEFAULT']['PLAY_SOUND_ENABLE']));
config['DEFAULT']['STARTUP_DEFAULT_UCL'] = str(int(config['DEFAULT']['STARTUP_DEFAULT_UCL']));
config['DEFAULT']['ENABLE_HALF_FULL'] = str(int(config['DEFAULT']['ENABLE_HALF_FULL']));

# merge f_arr and f_big5_arr
config['DEFAULT']['SEND_KIND_1_PASTE'] = my.trim(config['DEFAULT']['SEND_KIND_1_PASTE'])
config['DEFAULT']['SEND_KIND_1_PASTE'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_1_PASTE'])
config['DEFAULT']['SEND_KIND_2_BIG5'] = my.trim(config['DEFAULT']['SEND_KIND_2_BIG5'])
config['DEFAULT']['SEND_KIND_2_BIG5'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_2_BIG5'])
config['DEFAULT']['SEND_KIND_3_NOUCL'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_3_NOUCL'])

if config['DEFAULT']['SEND_KIND_1_PASTE'] != "": 
  f_arr = f_arr + my.explode(",",config['DEFAULT']['SEND_KIND_1_PASTE'])
if config['DEFAULT']['SEND_KIND_2_BIG5'] != "": 
  f_big5_arr = f_big5_arr + my.explode(",",config['DEFAULT']['SEND_KIND_2_BIG5'])
if config['DEFAULT']['SEND_KIND_3_NOUCL'] != "": 
  f_pass_app = f_pass_app + my.explode(",",config['DEFAULT']['SEND_KIND_3_NOUCL'])  


if int(config['DEFAULT']['KEYBOARD_VOLUME']) < 0:
  config['DEFAULT']['KEYBOARD_VOLUME'] = "0"
if int(config['DEFAULT']['KEYBOARD_VOLUME']) > 100:
  config['DEFAULT']['KEYBOARD_VOLUME'] = "100"
  
#debug_print(f_arr)
#debug_print(f_big5_arr)

# array_unique
# 2021-07-22 防止使用者在 f_arr 這些打多的逗號、空白
f_arr = my.array_remove_empty_and_trim(list(set(f_arr)))
f_big5_arr = my.array_remove_empty_and_trim(list(set(f_big5_arr)))
f_pass_app = my.array_remove_empty_and_trim(list(set(f_pass_app)))

#debug_print(f_arr)
#debug_print(f_big5_arr)

if float(config['DEFAULT']['ALPHA'])>=1:
  config['DEFAULT']['ALPHA']="1"
if float(config['DEFAULT']['ALPHA'])<=0.1:
  config['DEFAULT']['ALPHA']="0.1"

if float(config['DEFAULT']['NON_UCL_ALPHA'])>=1:
  config['DEFAULT']['NON_UCL_ALPHA']="1"
if float(config['DEFAULT']['NON_UCL_ALPHA'])<=0:
  config['DEFAULT']['NON_UCL_ALPHA']="0"  
  
if int(config['DEFAULT']['SHORT_MODE'])>=1:
  config['DEFAULT']['SHORT_MODE']="1"
if int(config['DEFAULT']['SHORT_MODE'])<=0:
  config['DEFAULT']['SHORT_MODE']="0"
  
if float(config['DEFAULT']['ZOOM'])>=3:
  config['DEFAULT']['ZOOM']="3"
if float(config['DEFAULT']['ZOOM'])<=0.1:
  config['DEFAULT']['ZOOM']="0.1"

if int(config['DEFAULT']['SP'])<=0:
  config['DEFAULT']['SP']="0"  
else:
  config['DEFAULT']['SP']="1"

if int(config['DEFAULT']['SHOW_PHONE_CODE'])<=0:
  config['DEFAULT']['SHOW_PHONE_CODE']="0"  
else:
  config['DEFAULT']['SHOW_PHONE_CODE']="1"
  
if int(config['DEFAULT']['CTRL_SP'])<=0:
  config['DEFAULT']['CTRL_SP']="0"  
else:
  config['DEFAULT']['CTRL_SP']="1"    

if int(config['DEFAULT']['PLAY_SOUND_ENABLE'])<=0:
  config['DEFAULT']['PLAY_SOUND_ENABLE']="0"  
else:
  config['DEFAULT']['PLAY_SOUND_ENABLE']="1"  

if int(config['DEFAULT']['STARTUP_DEFAULT_UCL'])<=0:
  config['DEFAULT']['STARTUP_DEFAULT_UCL']="0"  
else:
  config['DEFAULT']['STARTUP_DEFAULT_UCL']="1"    

if int(config['DEFAULT']['ENABLE_HALF_FULL'])<=0:
  config['DEFAULT']['ENABLE_HALF_FULL']="0"  
else:
  config['DEFAULT']['ENABLE_HALF_FULL']="1"    

# GUI Font
GLOBAL_FONT_FAMILY = "Mingliu,Serif,Malgun Gothic,roman" #roman
GUI_FONT_12 = {"FONT_NAME": GLOBAL_FONT_FAMILY, "FONT_SIZE": int( float(config['DEFAULT']['ZOOM'])*12), "FONT_WEIGHT": wx.NORMAL };
GUI_FONT_14 = {"FONT_NAME": GLOBAL_FONT_FAMILY, "FONT_SIZE": int( float(config['DEFAULT']['ZOOM'])*14), "FONT_WEIGHT": wx.BOLD };
GUI_FONT_16 = {"FONT_NAME": GLOBAL_FONT_FAMILY, "FONT_SIZE": int( float(config['DEFAULT']['ZOOM'])*16), "FONT_WEIGHT": wx.BOLD };
GUI_FONT_18 = {"FONT_NAME": GLOBAL_FONT_FAMILY, "FONT_SIZE": int( float(config['DEFAULT']['ZOOM'])*18), "FONT_WEIGHT": wx.BOLD };
GUI_FONT_20 = {"FONT_NAME": GLOBAL_FONT_FAMILY, "FONT_SIZE": int( float(config['DEFAULT']['ZOOM'])*20), "FONT_WEIGHT": wx.BOLD };
GUI_FONT_22 = {"FONT_NAME": GLOBAL_FONT_FAMILY, "FONT_SIZE": int( float(config['DEFAULT']['ZOOM'])*22), "FONT_WEIGHT": wx.BOLD };
GUI_FONT_26 = {"FONT_NAME": GLOBAL_FONT_FAMILY, "FONT_SIZE": int( float(config['DEFAULT']['ZOOM'])*26), "FONT_WEIGHT": wx.BOLD };
# print config setting
debug_print("UCLLIU.ini SETTING:")
debug_print("X:%s" % (config["DEFAULT"]["X"]))
debug_print("Y:%s" % (config["DEFAULT"]["Y"]))
debug_print("ALPHA:%s" % (config["DEFAULT"]["ALPHA"]))
debug_print("NON_UCL_ALPHA:%s" % (config["DEFAULT"]["NON_UCL_ALPHA"]))
debug_print("SHORT_MODE:%s" % (config["DEFAULT"]["SHORT_MODE"]))
debug_print("ZOOM:%s" % (config["DEFAULT"]["ZOOM"]))
debug_print("SEND_KIND_1_PASTE:%s" % (config["DEFAULT"]["SEND_KIND_1_PASTE"]))
debug_print("SEND_KIND_2_BIG5:%s" % (config["DEFAULT"]["SEND_KIND_2_BIG5"]))
debug_print("SP:%s" % (config["DEFAULT"]["SP"]))
debug_print("SHOW_PHONE_CODE:%s" % (config["DEFAULT"]["SHOW_PHONE_CODE"]))

def saveConfig():
  global config
  global INI_CONFIG_FILE
  with open(INI_CONFIG_FILE, 'w') as configfile:
    config.write(configfile)
def run_big_small(kind):
  global config
  global GLOBAL_FONT_FAMILY
  global GUI_FONT_12
  global GUI_FONT_14
  global GUI_FONT_16
  global GUI_FONT_18
  global GUI_FONT_20
  global GUI_FONT_22
  global GUI_FONT_26
  global simple_btn
  global x_btn
  global gamemode_btn
  global uclen_btn
  global hf_btn
  global type_label
  global word_label
  global play_ucl_label
  global ucl_find_data
  play_ucl_label=""
  ucl_find_data=[]
  type_label_set_text()
  toAlphaOrNonAlpha()
  
  kind = float(kind)
  if kind > 0:
    if float(config['DEFAULT']['ZOOM']) < 3:
      config['DEFAULT']['ZOOM'] = str(float(config['DEFAULT']['ZOOM'])+kind)
  else:
    if float(config['DEFAULT']['ZOOM']) > 0.3:
      config['DEFAULT']['ZOOM'] = str(float(config['DEFAULT']['ZOOM'])+kind)
  
  #GUI_FONT_12 = my.utf8tobig5("%s %d" % (GLOBAL_FONT_FAMILY,int( float(config['DEFAULT']['ZOOM'])*12) ));
  #GUI_FONT_14 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*14) ));
  #GUI_FONT_16 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*16) ));
  #GUI_FONT_18 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*18) ));
  #GUI_FONT_20 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*20) ));
  #GUI_FONT_22 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*22) ));
  #GUI_FONT_26 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*26) ));  
  
  if is_simple():    
    simple_btn.SetMinSize((0 ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
  simple_btn.SetFont(wx.Font(int(GUI_FONT_16["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_16["FONT_WEIGHT"],False,GUI_FONT_16["FONT_NAME"]))
  
  x_btn.SetFont(wx.Font(int(GUI_FONT_14["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_14["FONT_WEIGHT"],False,GUI_FONT_14["FONT_NAME"]))  
  x_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
  
  gamemode_btn.SetFont(wx.Font(int(GUI_FONT_12["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_12["FONT_WEIGHT"],False,GUI_FONT_12["FONT_NAME"]))  
  gamemode_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*80) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
    
  
  uclen_btn.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))  
  uclen_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
  
  
  hf_btn.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))  
  hf_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
  
  
  type_label.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))  
  type_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*100) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
  
  word_label.SetFont(wx.Font(int(GUI_FONT_20["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_20["FONT_WEIGHT"],False,GUI_FONT_20["FONT_NAME"]))  
  word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*350) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
          
  saveConfig()
    
def play_sound():  
  global m_play_song
  global max_thread___playMusic_counts
  global step_thread___playMusic_counts
  #global NOW_VOLUME
  global o_song
  global PWD
  global paudio_player
  if paudio_player == None:
    
    paudio_player = pyaudio.PyAudio()
  
  
  m_play_song.extend( [ random.choice(o_song.keys()) ])
  if len(o_song.keys())!=0 and step_thread___playMusic_counts < max_thread___playMusic_counts:
    step_thread___playMusic_counts = step_thread___playMusic_counts + 1
                      
    NOW_VOLUME = (int(config['DEFAULT']['KEYBOARD_VOLUME'])) #音量
    thread.start_new_thread( thread___playMusic,(NOW_VOLUME,))

def run_short():
  global config
  global word_label
  global type_label
  global gamemode_btn
  global play_ucl_label
  global ucl_find_data
  
  play_ucl_label=""
  ucl_find_data=[]
  type_label_set_text()
  toAlphaOrNonAlpha()
  
  word_label.Show(False)
  type_label.Show(False)
  gamemode_btn.Show(False)
  config["DEFAULT"]["SHORT_MODE"]="1"
  
  
  saveConfig()
def run_long():
  global config
  global word_label
  global type_label
  global gamemode_btn
  global play_ucl_label
  global ucl_find_data
  
  play_ucl_label=""
  ucl_find_data=[]
  type_label_set_text()
  toAlphaOrNonAlpha()
   
  word_label.Show(True)
  type_label.Show(True)
  gamemode_btn.Show(True)
      
  type_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*100) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
  word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*380) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
  
  config["DEFAULT"]["SHORT_MODE"]="0"
  saveConfig()

saveConfig()    
#check if exists tab cin json
is_need_trans_tab = False
is_need_trans_cin = False
is_all_fault = False
#my.unlink("liu.json")
#my.unlink("liu.cin")
if my.is_file(PWD + "\\liu.json") == False:
  if my.is_file(PWD + "\\liu.cin") == False:
    if my.is_file(PWD + "\\liu-uni.tab") == False:
      is_all_fault=True
    else:
      is_need_trans_tab=True
      is_need_trans_cin=True   
  else:
    is_need_trans_cin=True  

if is_all_fault==True and my.is_file("C:\\windows\\SysWOW64\\liu-uni.tab")==True:
  my.copy("C:\\windows\\SysWOW64\\liu-uni.tab",PWD+"\\liu-uni.tab")
  is_all_fault=False
  is_need_trans_tab=True
  is_need_trans_cin=True
  
if is_all_fault==True and my.is_file("C:\\Program Files\\BoshiamyTIP\\liu-uni.tab")==True:
  my.copy("C:\\Program Files\\BoshiamyTIP\\liu-uni.tab",PWD+"\\liu-uni.tab")
  is_all_fault=False
  is_need_trans_tab=True
  is_need_trans_cin=True

# 2019-04-13 加入 小小輸入法臺灣包2018年版wuxiami.txt，http://fygul.blogspot.com/2018/05/yong-tw2018.html 裡linux包中的/tw/wuxiami.txt
if is_all_fault==True and my.is_file(PWD + "\\wuxiami.txt")==True:
  debug_print("Run wuxiami.txt ...");
  my.copy(PWD+"\\wuxiami.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  m = my.explode("#修正錯誤：2018-4-15,17",data);
  data = my.trim(m[1])
  data = my.str_replace("\t"," ",data);
  data = my.implode("\n",m);  
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;  
# 2018-06-25 加入 RIME liur_trad.dict.yaml 表格支援
if is_all_fault==True and my.is_file(PWD + "\\liur_trad.dict.yaml")==True:
  debug_print("Run Rime liur_trad.dict.yaml ...");
  my.copy(PWD+"\\liur_trad.dict.yaml",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  # 2021-03-21
  # 不知道為啥 rime 要把好字的打改成 ~ 開頭@_@?
  data = my.str_replace("~","",data); 
  # 2021-03-21
  # 修正 ... 因為字根裡也有 ... 笑死 XD
  m = my.explode("#字碼格式: 字 + Tab + 字碼",data);
  data = my.trim(m[1])
  data = my.str_replace("\t"," ",data);
  # swap field
  m = my.explode("\n",data);
  for i in range(1,len(m)):
    d = my.explode(" ",m[i]);
    m[i] = "%s %s" % (d[1],d[0]);
  data = my.implode("\n",m);  
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;
  
# 2018-04-08 加入 terry 表格支援
if is_all_fault==True and my.is_file(PWD + "\\terry_boshiamy.txt")==True:
  #將 terry_boshiamy.txt 轉成 正常的 liu.cin、然後轉成 liu.json
  debug_print("Run terry ...")
  my.copy(PWD+"\\terry_boshiamy.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  m = my.explode("## 無蝦米-大五碼-常用漢字：",data);
  data = my.trim(m[1])
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;
  
  
# 2018-03-22 加入 fcitx 輸入法支援
if is_all_fault==True and my.is_file(PWD + "\\fcitx_boshiamy.txt")==True:
  #將 fcitx_boshiamy.txt 轉成 正常的 liu.cin、然後轉成 liu.json
  debug_print("Run fcitx ...")
  my.copy(PWD+"\\fcitx_boshiamy.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  data = my.str_replace("键码=,.'abcdefghijklmnopqrstuvwxyz[]\n","",data);
  data = my.str_replace("码长=5\n","",data);
  data = my.str_replace("[数据]",'''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''',data);
  #這版的日文很怪，正常的 a, 、 s, 都有怪字，我看全拿掉，用 j開頭的版本
  bad_words = [];
  res = re.findall('^(?!j)(\w+[,\.]\w*) (.*)\n',data,re.M);
  for k in res:
    d=" ".join(k);
    bad_words.append(d);
  #然後修正看不到的奇怪字
  #bad_words = ['','','','']
  mdata = my.explode("\n",data);
  new_mdata = [];
  for line in mdata:
    if not any(bad_word in line for bad_word in bad_words):
      new_mdata.append(line);
  data = my.implode("\n",new_mdata);
  #然後修正日文 ja, = あ 也相容 a, = あ
  res = re.findall('j(\w*[,\.]) (.*)\n',data,re.M);
  #debug_print(res) 
  for k in res:
    d=" ".join(k);
    data = data + d +"\n";  
  data = data + "%chardef end";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;  
  
if is_all_fault == True:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("無字根檔，請購買正版嘸蝦米，將「C:\\windows\\SysWOW64\\liu-uni.tab」或「C:\\Program Files\\BoshiamyTIP\\liu-uni.tab」與uclliu.exe放在一起執行")  
  response = message.run()
  #debug_print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    my.exit()
  #message.show()
  gtk.main()
           
if is_need_trans_tab==True:
  #需要轉tab檔                                                                             
  #Check liu-uni.tab md5 is fuck up
  if md5_file( ("%s\\liu-uni.tab" % (PWD)) )== "4e89501681ba0405b4c0e03fae740d8c":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("請不要使用義守大學的字根檔，這組 liu-uni.tab 太舊不支援...");
    response = message.run()
    #debug_print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      ctypes.windll.user32.PostQuitMessage(0)
      #atexit.register(cleanup)
      #os.killpg(0, signal.SIGKILL)
      my.exit()
    #message.show()
    gtk.main()
  # 2021-08-20 135、https://www.csie.ntu.edu.tw/~b92025/liu/ 裡的 liu-uni.tab 異常，利用 MD5 排除
  if md5_file( ("%s\\liu-uni.tab" % (PWD)) )== "41c458e859524613ca5e958f3d809b86":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("此組字根檔 (b92025) 並非主字根檔 liu-uni.tab，不支援...");
    response = message.run()
    #debug_print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      ctypes.windll.user32.PostQuitMessage(0)
      #atexit.register(cleanup)
      #os.killpg(0, signal.SIGKILL)
      my.exit()
    #message.show()
    gtk.main()
  if md5_file( ("%s\\liu-uni.tab" % (PWD)) )== "260312958775300438497e366b277cb4":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("此組字根檔並非正常的 liu-uni.tab，這個不支援...");
    response = message.run()
    #debug_print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      ctypes.windll.user32.PostQuitMessage(0)
      #atexit.register(cleanup)
      #os.killpg(0, signal.SIGKILL)
      my.exit()
    #message.show()
    gtk.main()
  import liu_unitab2cin
  #debug_print(PWD)  
  liu_unitab2cin.convert_liu_unitab( ("%s\\liu-uni.tab" % (PWD)), ("%s\\liu.cin" % (PWD) ))

if is_need_trans_cin==True:
  import cintojson
  cinapp = cintojson.CinToJson()
  cinapp.run( "liu" , "liu.cin",False)


last_key = "" #to save last 7 word for game mode
flag_is_capslock_down=False
flag_is_play_capslock_otherkey=False 
flag_is_win_down=False
flag_is_shift_down=False
flag_is_ctrl_down=False
flag_is_alt_down=False
flag_is_play_otherkey=False
flag_shift_down_microtime=0
flag_isCTRLSPACE=False
play_ucl_label=""
ucl_find_data=[]
pinyi_version="0" #初版
uclcode_phone = {}  #注音文字儲這 "-3": ["爾","耳","洱","餌","邇","珥","駬","薾","鉺","峏","尒","栮"]
re_uclcode_phone = {}  #注音文字儲這 "爾": ["ㄦˇ"]
is_need_use_phone=False
phone_INDEX = ", - . / 0 1 2 3 4 5 6 7 8 9 ; a b c d e f g h i j k l m n o p q r s t u v w x y z"
phone_DATA = "ㄝ ㄦ ㄡ ㄥ ㄢ ㄅ ㄉ ˇ ˋ ㄓ ˊ ˙ ㄚ ㄞ ㄤ ㄇ ㄖ ㄏ ㄎ ㄍ ㄑ ㄕ ㄘ ㄛ ㄨ ㄜ ㄠ ㄩ ㄙ ㄟ ㄣ ㄆ ㄐ ㄋ ㄔ ㄧ ㄒ ㄊ ㄌ ㄗ ㄈ"
phone_INDEX = my.explode(" ",phone_INDEX)
phone_DATA = my.explode(" ",phone_DATA)
same_sound_data=[] #同音字表
same_sound_index=0 #預設第零頁
same_sound_max_word=6 #一頁最多五字
is_has_more_page=False #是否還有下頁
same_sound_last_word="" #lastword


wavs = my.glob(PWD + "\\*.wav")
#debug_print("PWD : %s" % (PWD))
#debug_print(wavs)
o_song = {}
m_play_song = []
max_thread___playMusic_counts = 3 #最多同時五個執行緒在作動
step_thread___playMusic_counts = 0 #目前0個執行緒
for i in range(0,len(wavs)):
  #from : https://pythonbasics.org/python-play-sound/
  #m_song.extend([ AudioSegment.from_wav(wavs[i]) ])
  o_song[ wavs[i] ] = {
                        "lastKey": None,
                        "mainname" : my.mainname(wavs[i]).lower(),
                        "filename":wavs[i],
                        "data":[],
                        "wf":"",
                        "paudio_stream":""      
                      }
  if o_song[ wavs[i] ]["mainname"] == "enter" or o_song[ wavs[i] ]["mainname"] == "return":
    o_song[ wavs[i] ]["lastKey"]=13;
  elif o_song[ wavs[i] ]["mainname"] == "delete" or o_song[ wavs[i] ]["mainname"] == "del":
    o_song[ wavs[i] ]["lastKey"]=46;
  elif o_song[ wavs[i] ]["mainname"] == "backspace" or o_song[ wavs[i] ]["mainname"] == "bs":
    o_song[ wavs[i] ]["lastKey"]=8;
  elif o_song[ wavs[i] ]["mainname"] == "space" or o_song[ wavs[i] ]["mainname"] == "sp":
    o_song[ wavs[i] ]["lastKey"]=32;
#debug_print(my.json_encode(o_song))                      
#debug_print(PWD)
#debug_print(list(m_song))
#my.exit()
# 用來出半型字的
# https://stackoverflow.com/questions/2422177/python-how-can-i-replace-full-width-characters-with-half-width-characters
HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
                  
def widen(s):
  #https://gist.github.com/jcayzac/1485005
  """
  Convert all ASCII characters to the full-width counterpart.
  
  >>> print widen('test, Foo!')
  ｔｅｓｔ，　Ｆｏｏ！
  >>> 
  """
  return str(s).translate(WIDE_MAP)
def load_phone(pinyi_filepath):
  data = my.file_get_contents(pinyi_filepath)
  data = my.trim(data.replace("\r",""))
  output = {}
  m = my.explode("\n",data)
  if len(m)<3:
    return
  for i in range(3,len(m)):
    d = my.explode(" ",m[i]);
    d[0] = str(d[0])
    output[d[0]] = my.explode(" ",m[i])[1:]
    for j in range(0,len(output[d[0]])):
      output[d[0]][j] = str(output[d[0]][j])
  return output
def re_load_phone(_uclcode_phone):
  # 有點慢，考慮放到 thread 跑
  #把
  #uclcode_phone = {}  #注音文字儲這 "-3": ["爾","耳","洱","餌","邇","珥","駬","薾","鉺","峏","尒","栮"]
  #轉成
  #re_uclcode_phone = {}  #注音文字儲這 "爾": ["ㄦˇ"]
  #global re_uclcode_phone
  output = {}
  for k in uclcode_phone:
    #debug_print(k)
    #debug_print(uclcode_phone[k])
    #wj/
    #[u'\u901a', u'\u606b', u'\u84ea', u'\u75cc', u'\u70b5', u'\u71a5', u'\u72ea']    
    #my.exit()
    # k = wj/
    for kv in uclcode_phone[k]:
      #kv = kv
      #debug_print(kv); #通
      #my.exit()
      #if kv not in output:
      if kv not in output:
        output[kv] = []
      # 取得 注音 wj/ -> ㄊㄨˊ
      #debug_print(k)
      #my.exit()        
      k_phone = phone_en_to_code(k)      
      #debug_print(k_phone)
      #my.exit()      
      if k_phone not in output[kv]:        
        output[kv].append(k_phone)
    #debug_print(output)    
    #my.exit()
  #my.exit() 
  #pass
  #debug_print(output[u"肥"][0]) # 出 ㄈㄟˊ
  #my.exit()
  #re_uclcode_phone = output
  return output  
#debug_print((re_uclcode_phone=={})) # 得 True
#my.exit()
#a = {}
#debug_print(a.has_key("abc"))
#my.exit()
def phone_en_to_code(_en):
  #注音的英數，轉注音，如 -3 -> ㄦˇ
  global phone_DATA
  global phone_INDEX
  # 已轉陣列
  #phone_INDEX = [, - . / 0 1 2 3 4 5 6 7 8 9 ; a b c d e f g h i j k l m n o p q r s t u v w x y z]
  #phone_DATA =  [ㄝ ㄦ ㄡ ㄥ ㄢ ㄅ ㄉ ˇ ˋ ㄓ ˊ ˙ ㄚ ㄞ ㄤ ㄇ ㄖ ㄏ ㄎ ㄍ ㄑ ㄕ ㄘ ㄛ ㄨ ㄜ ㄠ ㄩ ㄙ ㄟ ㄣ ㄆ ㄐ ㄋ ㄔ ㄧ ㄒ ㄊ ㄌ ㄗ ㄈ]
  #m = mystts.split_unicode_chrs(_en);
  m = list(_en);
  output = ""
  for i in range(0,len(m)):              
    m[i] = phone_DATA[phone_INDEX.index(m[i])]
  output = my.implode("",m)
  output = str(output)
  return output 
#debug_print("phone_en_to_code(\"-3\"): %s" % str(phone_en_to_code("-3"))) # 出「ㄦˇ」OK  
#debug_print("phone_en_to_code(\"wj/\"): %s" % str(phone_en_to_code("wj/"))) # phone_en_to_code("wj/"): ㄊㄨㄥ
#my.exit();
def phone_to_en_num(phone_code):
  #注音轉回英數 ㄦˇ -> -3
  global phone_DATA
  global phone_INDEX
  phone_code = phone_code
  m = mystts.split_unicode_chrs(phone_code);
  output = ""  
  for i in range(0,my.strlen(m)):              
    m[i] = phone_INDEX[phone_DATA.index(m[i])]
  output = my.implode("",m)  
  return output 
#def pleave(self, event):
#  my.exit();

if my.is_file(PWD + "\\liu.json") == False:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("缺少liu.json")  
  response = message.run()
  #debug_print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    my.exit()
  #message.show()
  gtk.main()
  #my.exit()
if my.is_file(PWD + "\\pinyi.txt")==True:
  same_sound_data = my.explode("\n",my.trim(my.file_get_contents(PWD + "\\pinyi.txt")))
  if my.is_string_like(same_sound_data[0],"VERSION_0.01"):
      pinyi_version = "0.01";
      # 載入uclcode_phone
      uclcode_phone = load_phone(PWD + "\\pinyi.txt")
      # 稍慢 +2 sec
      #thread.start_new_thread( re_load_phone, (uclcode_phone, ))
      re_uclcode_phone = re_load_phone(uclcode_phone)
      #debug_print(uclcode_phone)
  
uclcode = my.json_decode(my.file_get_contents(PWD + "\\liu.json"))

uclcode_r = {}
uclcode_rr = {}
#然後把 chardefs 的字碼，變成對照字根，可以加速 ,,,z、,,,x 反查的速度
#only short key
_vrsfw_arr = ['v','r','s','f','w','l','c','b','k','j','je','jr','js','jf','jw','jl','jc','jb','jk','rj','re','rr']

# 192、韓語字根在 liu.json 裡有些 key 是大寫，載入時改全小寫再使用，如：녕 sUd.
# UCL key 強制轉小寫，有大寫的都移除
keys_to_delete = []
for k, v in uclcode["chardefs"].items():
    lower_k = k.lower()
    if k != lower_k:
        uclcode["chardefs"][lower_k] = v
        keys_to_delete.append(k)
for k in keys_to_delete:
    del uclcode["chardefs"][k]
    
for k in uclcode["chardefs"]:         
   #2022-09-01 感謝 Benson9954029 提出修正
   for kk in range(0,len(uclcode["chardefs"][k])):
     _word = uclcode["chardefs"][k][kk]
     temp_k = k     
     if kk > 0: # and kk-1 < len(_vrsfw_arr):       
       # 如 娚-> gqd2
       #debug_print("str(kk) : "+str(kk));
       temp_k = str(str(k)+str(kk))
       # 如 娚-> gqd2 -> gqdr
       #temp_k = str(str(k)+str(_vrsfw_arr[kk-1]))
       #debug_print("temp_k : "+temp_k);
       #debug_print("str(k) : "+str(k));
       #debug_print("str(kk) : "+str(kk));
       #sys.exit();
       #temp_k : gai1
       #str(k) : gai
       #str(kk) : 1
     if _word not in uclcode_r:
       uclcode_r[_word] = temp_k
       uclcode_rr[temp_k] = _word
     else:
       if len(temp_k) < len(uclcode_r[_word]):
         uclcode_r[_word] = temp_k         
         uclcode_rr[temp_k] = _word
     #debug_print(_word + ", " + uclcode_r[_word]);  # 媮, gai
     #debug_print(temp_k + ", " + uclcode_rr[temp_k]);  # gai, 媮
     #my.exit()
     #if _word == '夬' or _word == '搉':
     #    debug_print(uclcode_r[_word] + ":"+ _word)
#my.exit()        


def thread___playMusic(keyboard_volume):
  global lastKey
  global PWD
  #try:
  # https://stackoverflow.com/questions/43679631/python-how-to-change-audio-volume
  # 調整聲音大小
  # https://stackoverrun.com/cn/q/10107660
  # Last : https://www.thinbug.com/q/45219574
  global paudio_player
  global o_song
  global m_play_song
  global is_sound_playing
  global sound_playing_s
  #global wave
  global step_thread___playMusic_counts   
  try:                   
    if len(m_play_song) !=0 :      
      # https://stackoverflow.com/questions/36664121/modify-volume-while-streaming-with-pyaudio
      chunk = 2048
      #s = random.choice(m_song)
      #debug_print(my.json_encode(m_play_song))                    
      #m_play_song = m_play_song[ : 2]
      #s = m_play_song.pop(0) #m_play_song[0]   
  
      #debug_print("lastKey")
      #debug_print(lastKey)      
      s = ""
      if my.in_array(lastKey,[13,46,32,8]):
        for key in o_song:
          #debug_print("Key")
          #debug_print(key)
          #debug_print(o_song[key]["lastKey"])
          if o_song[key]["lastKey"]!=None and o_song[key]["lastKey"] == lastKey:
            s = key
            #debug_print("s")
            #debug_print(s)  
            break;     
      if s == "":
        _arr = []
        for key in o_song:
          if o_song[key]["lastKey"]==None:
            _arr.append(key)
          pass
        s = _arr[my.rand(0,len(_arr)-1)]
        
      #debug_print(my.json_encode(s))      
      #return     
      if len(o_song[s]["data"]) == 0 or o_song[s]["volume"] != keyboard_volume:        
        o_song[s]["volume"] = keyboard_volume
        o_song[s]["data"] = []
        debug_print("wave s: %s" % (s) )
        o_song[s]["wf"] = wave.open(s, 'rb')
        o_song[s]["paudio_stream"] = paudio_player.open(format = paudio_player.get_format_from_width(o_song[s]["wf"].getsampwidth()),
                      channels = o_song[s]["wf"].getnchannels(),
                      rate = o_song[s]["wf"].getframerate(),
                      output = True)
        # 寫聲音檔輸出來播放
        
        while True:
          #if is_sound_playing == False:            
          #  sound_playing_s = s
          #  is_sound_playing = True
          #elif is_sound_playing == True and sound_playing_s != s:
          #  break;          
          d = o_song[s]["wf"].readframes(chunk)
          if d == "": 
            break      
          # 這是調整音量大小的方法
          o_song[s]["data"].extend([ audioop.mul(d, 2, keyboard_volume / 100.0 ) ])
        #if is_sound_playing == True and sound_playing_s == s:
        #  sound_playing_s = ""
        #  is_sound_playing = False                    
      for i in range(0,len(o_song[s]["data"])):
        # 播放聲音的地方
        if is_sound_playing == False:            
          sound_playing_s = s
          is_sound_playing = True
        elif is_sound_playing == True and sound_playing_s != s:
          break;          
        o_song[s]["paudio_stream"].write(o_song[s]["data"][i])        
      if is_sound_playing == True and sound_playing_s == s:
         sound_playing_s = ""
         is_sound_playing = False
    if step_thread___playMusic_counts > 0:
      step_thread___playMusic_counts = step_thread___playMusic_counts -1         
  except Exception as e:
    thread___playMusic(keyboard_volume)
    #debug_print("thread___playMusic error:")
    #debug_print(e)    
           
def thread___x(data):
  #字根轉中文 thread  
  selectData=my.trim(data);  
  menter = my.explode("\n",selectData);
  output = "";
  for kLine in range(0,len(menter)):
    m = my.explode(" ", menter[kLine]);        
    #debug_print(len(m));
    for i in range(0,len(m)):
      #轉小寫
      ucl_split_code = my.strtolower(m[i])
      output += uclcode_to_chinese(ucl_split_code)
    if kLine != len(menter)-1:      
      output+="{ENTER}"
  senddata(output)  


def word_to_sp(data):
  #中文字串轉最簡字根
  #回傳字根文字
  #中文轉字根 thread  
  #debug_print("word_to_sp: ")
  #debug_print(data)
  selectData = data; #my.trim(data);
  selectData = selectData.replace("\r","");
  menter = my.explode("\n",selectData);
  
  output = "";
  for kLine in range(0,len(menter)):
    output_arr = []
    #debug_print(u"切斷前："+str(menter[kLine]));
    m = mystts.split_unicode_chrs(menter[kLine]);
    #debug_print(u"切斷後：");
    #debug_print(m);
    for k in range(0,len(m)):
      _uclcode = find_ucl_in_uclcode(m[k]);
      if _uclcode!="":
        output_arr.append(_uclcode)  
    output += my.implode(" ",output_arr);    
    if kLine != len(menter)-1:      
      output+="{ENTER}"
  #debug_print(output)
  output = output.replace(" ","{SPACE}");
  output = output.replace("\n ","{ENTER}");  
  output = output.replace("\n","{ENTER}"); 
  return output 
def show_phone_to_label(data,isForce=None):
  #顯示注音到輸入結束框後
  #2023-02-18 
  #Issue. 171、網友 Allen 希望肥米打出文字後，可以提示「注音怎麼念」
  global config
  global play_ucl_label
  global re_uclcode_phone  
  if config['DEFAULT']['SHOW_PHONE_CODE']=="0" and isForce is None:
    return
  # 將傳入的 data 文字，取得注音念法
  m_phone_code = []
  if data in re_uclcode_phone:
    m_phone_code = re_uclcode_phone[data] # 如 data = 肥，取得 ["ㄈㄟˊ"]
  
  # 未知的讀音
  if len(m_phone_code)==0:
    return
  _str_read_phone = my.implode("或",m_phone_code)
  orin_label_text = word_label_get_text()
  if orin_label_text == "":
    #沒設簡根
    type_label_set_text("音:%s" % (_str_read_phone))
  else:
    type_label_set_text("%s,音:%s" % (orin_label_text,_str_read_phone))

def show_sp_to_label(data,isForce=None):
  #顯示最簡字根到輸入結束框後
  global config
  global play_ucl_label
  global _vrsfw_arr
  global uclcode_rr
  
  if config['DEFAULT']['SP']=="0" and isForce is None:
    return
  # 2022-09-02 如果末字是數字，可調整為 VRSFW
  #debug_print("show_sp_to_label...");
  #debug_print(data);
  
  _sp_data = my.strtoupper(word_to_sp(data))
  
  # H1 时
  #debug_print("_sp_data[:-1]: "+_sp_data[:-1]); # H
  #debug_print("_sp_data[-1]: "+_sp_data[-1]); # 1
  # Issue : 189、时(h1 提示根有 hv、h1) ，但 hv 實際是另一個字根「惟」(感謝 Benson9954029 回報)
  if len(_sp_data) > 0 and str(_sp_data[-1]).isnumeric() and int(_sp_data[-1])>=1 and int(_sp_data[-1])<=5:
    # 如果預選字，如 「GQD 動 舅 娚」的 kk 在 1 或 2 (舅、娚)，就會變 GQD1 GQD2     
    # 如為數字，加上 反 VRSFW 功能
    _tmp_sp_data = _sp_data[:-1] + my.strtoupper(_vrsfw_arr[int(_sp_data[-1])-1]) 
    # debug_print("_tmp_sp_data: %s + %s" % (_sp_data[:-1] , my.strtoupper(_vrsfw_arr[int(_sp_data[-1])-1])) ) # H + V
    # 為修正 Issue : 189 字根表 HV 如果沒有「时」，就不顯示
    #debug_print("uclcode_rr[\"hv\"]: %s" % (uclcode_to_chinese("hv"))); # 惟    
    #debug_print("data: %s" % (str(data)));
    #debug_print("uclcode_rr[\"pns\"]: %s" % (uclcode_rr["pns"])); # 你
    #debug_print("_sp_data: %s" % (_sp_data)); #H1
    #debug_print("_tmp_sp_data: %s" % (_tmp_sp_data)); # HV
    if my.strtolower(_tmp_sp_data) not in uclcode_rr:
      _sp_data = _tmp_sp_data + "或" + _sp_data
    else:
      pass
    #elif my.strtoupper(_sp_data[:-1] + my.strtoupper(_vrsfw_arr[int(_sp_data[-1])-1])) in uclcode_rr and  :
  sp = "簡:" + _sp_data 
  #word_label.SetLabel(sp)
  
  # Issue : 162、(評估中)自定詞，超過一個字以上，不需顯示簡根
  # 字根有包含 { 就不顯示
  # 自定字根，通常是多字，多字就會包含 {SPACE}
  if my.is_string_like(_sp_data,"{"):
    return
  type_label_set_text(sp)     
def thread___z(data):
  #debug_print("thread___z: ")
  #debug_print(data);  
  senddata(data)
       
def find_ucl_in_uclcode(chinese_data):
  #用中文反找蝦碼(V1.10版寫法)
  global uclcode_r
  global _vrsfw_arr
  #debug_print(u"用中文反找蝦碼(V1.10版寫法)");  
  chinese_data = str(chinese_data);
  if chinese_data in uclcode_r:
    #debug_print("chinese_data : " + str(chinese_data));
    #debug_print("uclcode_r[chinese_data] : " + str(uclcode_r[chinese_data]));
    # 如果字碼末字是數字，轉回 vrswf...
    _found_word = uclcode_r[chinese_data];
    #if len(_found_word) > 0 and str(_found_word[-1]).isnumeric() and int(_found_word[-1])>=1 and int(_found_word[-1])<=5:
    #  _found_word = _found_word[:-1] + _vrsfw_arr[int(_found_word[-1])-1]
    return _found_word 
  else:
    return chinese_data;
     
#def find_ucl_in_uclcode_old(chinese_data):
#  #用中文反找蝦碼(V1.9版寫法)
#  finds = []  
#  for k in uclcode["chardefs"]:
#    if chinese_data in uclcode["chardefs"][k]:
#      index = uclcode["chardefs"][k].index(chinese_data)
#      finds.append(k+"_"+str(index))
#  finds.sort(key=len, reverse=False)
#  
#  shorts_arr = []
#  shorts_len = 999;
#  for k in finds:
#    if len(shorts_arr)==0 or len(k) <=shorts_len :
#      if len(k) == shorts_len:
#        shorts_arr.append(k)
#        shorts_len = len(k)
#      else:
#        shorts_arr = []
#        shorts_arr.append(k)
#        shorts_len = len(k)
#  shorts_arr = sorted(shorts_arr, key = lambda x: int(x.split("_")[1]))
#  if len(shorts_arr) >= 1:
#    d = shorts_arr[0].split("_")
#    return d[0]        
#  else:
#    return "";

#debug_print(find_ucl_in_uclcode("肥"))
#my.exit();
def UCLGUI_GET_TASKBAR_HEIGHT():
  monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
  monitor_area = monitor_info.get("Monitor")
  work_area = monitor_info.get("Work")
  return (monitor_area[3]-work_area[3])
def UCLGUI_CLOSEST_MONITOR():
  global myScreenStatus
  #肥米靠近哪個螢幕
  [ _x,_y ] = win.GetPosition()
  [_width,_height] = win.GetSize()
  #肥米中心點
  UCL_c_x = _x + ( _width / 2 );
  UCL_c_y = _y + ( _height / 2 );
  _UCL_Closest_Monitor_NO = 0; #哪一個螢幕            
  _UCL_Closest_Monitor_Distinct = 0; #距離    
  for i in range(0, len(myScreenStatus["screens"])):
    if i == 0:
      _UCL_Closest_Monitor_NO = i
      #距離 = ((x1-x2)^2 + (y1-y2)^2) ** 0.5
      _UCL_Closest_Monitor_Distinct = (  (UCL_c_x-myScreenStatus["screens"][i]["c_x"]) ** 2 + (UCL_c_y-myScreenStatus["screens"][i]["c_y"]) ** 2 ) ** 0.5; 
    else:
      _distinct = (  (UCL_c_x-myScreenStatus["screens"][i]["c_x"]) ** 2 + (UCL_c_y-myScreenStatus["screens"][i]["c_y"]) ** 2 ) ** 0.5;
      if _distinct < _UCL_Closest_Monitor_Distinct:
        _UCL_Closest_Monitor_Distinct = _distinct
        _UCL_Closest_Monitor_NO = i
  return _UCL_Closest_Monitor_NO      
        
def toAlphaOrNonAlpha():
  global uclen_btn
  global hf_btn
  global win
  global config
  global user32 
  global win
  global app
  #2019-10-22 check screen size and uclliu position
  # 偵測肥米的位置，超出螢幕時，彈回
  #screen_width=user32.GetSystemMetrics(0)
  #screen_height=user32.GetSystemMetrics(1)  
  #screen_width = gtk.gdk.screen_width()
  #screen_height = gtk.gdk.screen_height()  
  
  #2021-07-27 改成偵測現在肥米離哪個螢幕中心點比較近，如果超過該螢幕限範圍回，要修正位置
  #debug_print("UCL Closest Monitor: %s\n" % (UCLGUI_CLOSEST_MONITOR()))
  #顯示該螢幕的 info
  #debug_print(my.json_encode(myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]))
  # {"area": 2764800, "h": 1080, "c_y": 540, "w": 2560, "c_x": 1280, "y": 0, "x": 0}
  
  [ _x,_y ] = win.GetPosition()
  [_width,_height] = win.GetSize()
  
  new_position_x = _x
  new_position_y = _y
  
  # 每次都重刷 DB ?
  myScreenStatus["screens"] = []
  #for i in range(0,myScreensObj.get_n_monitors()):
  for i, monitor in enumerate(monitors, 1):
    d = {
      "x": monitor.x,
      "y": monitor.y,
      "w": monitor.width,
      "h": monitor.height,
      "area": (monitor.width * monitor.height),
      "c_x": (monitor.x + (monitor.width / 2)),
      "c_y": (monitor.y + (monitor.height / 2))
    }
    myScreenStatus["screens"].append(d);  
  
  if _x  > (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["w"]) - _width:
    new_position_x = (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["w"])-_width-20    
    win.Move( (new_position_x,new_position_y))
  taskbar_height = UCLGUI_GET_TASKBAR_HEIGHT()
  if _y > (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["h"]) - _height - taskbar_height:
    new_position_y = (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["h"]) - _height - 20 - taskbar_height
    win.Move( (new_position_x,new_position_y))
  
  if _x < myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"]:
    new_position_x = myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"]+20;
    win.Move( (new_position_x,new_position_y))
  if _y < myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"]:
    new_position_y = myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"]+20
    win.Move( (new_position_x,new_position_y))
    
  if uclen_btn.GetLabel()=="英" and hf_btn.GetLabel()=="半":
    #win.set_opacity(0.2)
    #win.set_mnemonics_visible(True)
    #2021-12-01 增加 NON_UCL_ALPHA 來調整英數時的透明度
    #win.set_opacity( float(config["DEFAULT"]["NON_UCL_ALPHA"]) )
    win.SetTransparent( int(my.arduino_map(float(config["DEFAULT"]["NON_UCL_ALPHA"]),0,1.0,0,255 )))
    #win.set_keep_above(False)
    #win.set_keep_below(True) 
    win.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT)
  else:
    #win.set_opacity(1)
    #debug_print(win.get_opacity())
    #if float(win.get_opacity()) != float(config["DEFAULT"]["ALPHA"]): 
    #win.set_opacity( float(config["DEFAULT"]["ALPHA"]) )
    win.SetTransparent( int(my.arduino_map(float(config["DEFAULT"]["ALPHA"]),0,1.0,0,255 )))
    #debug_print(float(config["DEFAULT"]["ALPHA"]))
    #win.set_mnemonics_visible(True)
    #win.set_keep_above(True)
    #win.set_keep_below(False)
    win.SetWindowStyle(wx.STAY_ON_TOP)
    app.SetTopWindow(win)
  win.SetSizerAndFit(vbox)
def toggle_ucl():
  global uclen_btn
  global play_ucl_label
  global win
  global debug_print
  global GUI_FONT_22
  global is_need_use_phone
  global ucl_find_data
  #2021-08-31 
  #切換後，即關閉注音模式  
  is_need_use_phone = False
  is_need_use_pinyi = False  
  #2021-08-31
  #切換時，清空所有後選字
  ucl_find_data=[]
  if uclen_btn.GetLabel()=="肥":
    uclen_btn.SetLabel("英")
    play_ucl_label=""
    type_label_set_text()
    #win.set_keep_above(False)
    #win.set_keep_below(True)
    win.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT)
  else:
    uclen_btn.SetLabel("肥")
    #win.set_keep_above(True)
    #win.set_keep_below(False)
    win.SetWindowStyle(wx.STAY_ON_TOP)
  
  uclen_btn.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))
                                              
  #window_state_event_cb(None,None)
  debug_print("window_state_event_cb(toggle_ucl)")  
  toAlphaOrNonAlpha()    
def is_ucl():
  global uclen_btn  
  #print("WTF: %s" % uclen_btn.GetLabel())
  if uclen_btn.GetLabel()=="肥":
    return True
  else:
    return False
def is_simple():
  global simple_btn      
  #print("WTF simple: %s" % simple_btn.get_visible())
  #(w,h) = simple_btn.GetSize_request();  
  return simple_btn.Show()
      
def gamemode_btn_click(self):
  global gamemode_btn
  global tray 
  if gamemode_btn.GetLabel()=="正常模式":
    gamemode_btn.SetLabel("遊戲模式")
    if uclen_btn.GetLabel() == "肥":
      uclen_btn_click(uclen_btn)    
  else:
    gamemode_btn.SetLabel("正常模式")
  tray.reload_tray()
def x_btn_click(self):
  print("Bye Bye");
  global tray
  global FlagStopUpdateGUI
  FlagStopUpdateGUI = True
  #global menu
  #2021-08-08 no need change tray ?
  try:
    tray.systray.shutdown();
  except:
    pass
  #print(dir(tray))  
  #tray.Show(False)
  #menu.Show(False)
  try:
    ctypes.windll.user32.PostQuitMessage(0)
  except:
    pass
  #atexit.register(cleanup)
  #os.killpg(0, signal.SIGKILL)
  sys.exit(0)
# draggable
def winclicked(self, event):
  # make UCLLIU can draggable  
  self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  #self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  #self.window.begin_resize_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  # Write to UCLLIU.ini
  global config
  global win
  
  #_x = win.get_allocation().width
  #_y = win.get_allocation().height
  
  [ _x,_y ] = win.GetPosition()
  #debug_print( "x_root , y_root : %d , %d" % (event.x,event.y))
  #debug_print( "WIN X,Y:%d , %d" % (_x,_y)) 
  config["DEFAULT"]["X"] = str(int(_x))
  config["DEFAULT"]["Y"] = str(int(_y))
  debug_print( "config X,Y:%s , %s" % (config["DEFAULT"]["X"],config["DEFAULT"]["Y"])) 
  saveConfig();
  pass
def uclen_btn_click(self):
  toggle_ucl()
  #pass
def hf_btn_click(self):
  global GUI_FONT_22
  global hf_btn
  kind=hf_btn.GetLabel()
  if kind=="半":
    hf_btn.SetLabel("全")    
  else:
    hf_btn.SetLabel("半")      
  hf_btn.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))
  toAlphaOrNonAlpha()
  pass
def is_hf(self):
  global hf_btn
  kind=hf_btn.GetLabel()
  return (kind=="半")
   
# http://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
def type_label_get_text():
  global type_label
  return type_label.GetLabel();
def word_label_get_text():
  global word_label
  return word_label.GetLabel();
def type_label_set_text(last_word_label_txt="",showOnly=False):
  global type_label
  global word_label
  global play_ucl_label
  global debug_print
  global GUI_FONT_22
  global GUI_FONT_20
  global GUI_FONT_18
  global GUI_FONT_16
  global GUI_FONT_14
  global GUI_FONT_12
  global config
  global is_need_use_phone
  #debug_print("type_label_set_text");
  #debug_print(play_ucl_label);
  
  type_label.SetLabel(str(play_ucl_label))  
  type_label.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))
  
  if my.strlen(play_ucl_label) > 0:
    debug_print("ShowSearch")
    if is_need_use_phone == True:
      #debug_print("RUN PHONE")
      # 只有在發音時，才要 show_search      
      if showOnly == False:
        show_search("phone")
    else:
      show_search(None)
      word_label.SetForegroundColour(wx.Colour(0, 0, 0))
    pass
  else:
    if is_need_use_phone == True:
      #pass
      # 注音模式時，是藍色 label
      #type_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color("#007fff"))
      type_label.SetForegroundColour(wx.Colour(0, 127, 255))
      #word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color("#007fff"))
      word_label.SetForegroundColour(wx.Colour(0, 127, 255))
      # 注音輸入模式時，輸入區長度固定為 130
      if config["DEFAULT"]["SHORT_MODE"]=="0":
        if config["DEFAULT"]["SHORT_MODE"]=="0":
            word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*350) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
        else:
            word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*100) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
      word_label.SetLabel("注:")
    else:    
      # 非注音時，是黑色
      if config["DEFAULT"]["SHORT_MODE"]=="0":
        # 非注音模式，回到預設的長度        
        type_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*100) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
      #type_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color("#000000"))
      #word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
      type_label.SetForegroundColour(wx.Colour(0, 0, 0))
      word_label.SetForegroundColour(wx.Colour(0, 0, 0))
      word_label.SetLabel("")
    word_label.SetFont(wx.Font(int(GUI_FONT_20["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_20["FONT_WEIGHT"],False,GUI_FONT_20["FONT_NAME"]))
    
    pass
  # 如果 last_word_label_txt 不是空值，代表有簡根或其他用字  
  if last_word_label_txt != "":
    #2023-02-18 加入，如「的」(簡:D,音:ㄉㄦ˙或ㄉㄧˊ或ㄉㄧˋ...)
    debug_print("my.strlen(last_word_label_txt): %d" % (my.strlen(last_word_label_txt)))
    if my.strlen(last_word_label_txt)>14:      
      word_label.SetFont(wx.Font(int(GUI_FONT_16["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_16["FONT_WEIGHT"],False,GUI_FONT_16["FONT_NAME"]))
  
    word_label.SetLabel( last_word_label_txt )
    #word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color("#007fff"))
    word_label.SetForegroundColour(wx.Colour(0, 127, 255))
    
  #如果是短米，自動看幾個字展長
  if config["DEFAULT"]["SHORT_MODE"]=="1":
    _tape_label = type_label.GetLabel()
    _len_tape_label = len(_tape_label)
    #一字30
    if _len_tape_label == 0:
      type_label.Show(False)
    else:
      type_label.Show(True)    
    #type_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*28*_len_tape_label) ,(int(float(config['DEFAULT']['ZOOM'])*40 )))) 
    
    # 根據文字大小計算適當的控件大小
    type_label.SetMinSize(type_label.GetSizeFromTextSize(type_label.GetTextExtent(_tape_label))) 
    
    _word_label = word_label.GetLabel()
    _len_word_label = len(_word_label)
    #一字30
    if _len_word_label == 0:
      word_label.Show(False)
    else:
      word_label.Show(True)    
    #word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*25*_len_word_label) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
    # 根據文字大小計算適當的控件大小
    word_label.SetMinSize(word_label.GetSizeFromTextSize(word_label.GetTextExtent(_word_label)))
  return True
def word_label_set_text():
  global word_label
  global ucl_find_data   
  global play_ucl_label
  global is_has_more_page
  global GUI_FONT_20
  global GUI_FONT_18
  global GUI_FONT_16
  global GUI_FONT_14
  global GUI_FONT_12
  
  if play_ucl_label == "":
    word_label.SetLabel("")    
    word_label.SetFont(wx.Font(int(GUI_FONT_18["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_18["FONT_WEIGHT"],False,GUI_FONT_18["FONT_NAME"]))
    return
  step=0
  m = []
  try:  
    for k in ucl_find_data:
      m.append("%d%s" % (step,k))
      step=step+1
    tmp = my.implode(" ",m)
    if is_has_more_page == True:
      tmp = "%s ..." % (tmp)
    word_label.SetLabel(tmp)
    
    debug_print(("word_label lens: %d " % (len(tmp))));    
    lt = len(tmp);
    word_label.SetFont(wx.Font(int(GUI_FONT_20["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_20["FONT_WEIGHT"],False,GUI_FONT_20["FONT_NAME"]))
    
    if config["DEFAULT"]["SHORT_MODE"]=="1":
      _word_label = word_label.GetLabel()
      _len_word_label = len(_word_label)
      #一字30
      if _len_word_label == 0:
        word_label.Show(False)
      else:
        word_label.Show(True)
      if is_has_more_page==False:        
        #word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*12*_len_word_label) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
        word_label.SetMinSize(word_label.GetSizeFromTextSize(word_label.GetTextExtent(_word_label)))
      else:
        #有額外的分頁，加了...
        debug_print("More page...")        
        #word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*13*_len_word_label) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
        word_label.SetMinSize(word_label.GetSizeFromTextSize(word_label.GetTextExtent(_word_label)))
    return True
  except:
    play_ucl_label=""
    play_ucl("")
    word_label.SetLabel("")
    word_label.SetFont(wx.Font(int(GUI_FONT_18["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_18["FONT_WEIGHT"],False,GUI_FONT_18["FONT_NAME"]))
    return True
def uclcode_to_chinese(code):
  # 字根 轉 中文字
  global uclcode_rr
  if code in uclcode_rr:
    #debug_print("use : uclcode_to_chinese ... uclcode_rr");
    return uclcode_rr[code]
  #return code
  # 繼續走下面流程
  #debug_print(u"use : uclcode_to_chinese ... 繼續走下面流程");
  global ucl_find_data
  #global debug_print
  global _vrsfw_arr  
  c = code
  c = my.trim(c)
  if c == "":
    return ""
  # 如果最末碼是 1234567... 嘗試轉換 vrsfw...
  #if len(c)>=2 and str(c[-1]).isnumeric() and int(c[-1])>=1 and int(c[-1]) < 10:
  #  c = c[:-1] + _vrsfw_arr[int(c[-1])-1]
  #debug_print(c)
  if c not in uclcode["chardefs"] and c[-1]=='v' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=2 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][1]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='r' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=3 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][2]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='s' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=4 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][3]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='f' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=5 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][4]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='w' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=6 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][5]       
    return ucl_find_data
  elif c in uclcode["chardefs"]:
    #debug_print("Debug V2")
    ucl_find_data = uclcode["chardefs"][c][0]    
    return ucl_find_data
  else:    
    return code 
def show_search(kind):
  #真的要顯示了
  global play_ucl_label
  global ucl_find_data
  global ucl_find_data_orin_arr
  global is_need_use_pinyi
  global is_need_use_phone
  global is_has_more_page
  global same_sound_index
  global same_sound_last_word
  global debug_print
  global same_sound_max_word
  global uclcode_phone
  same_sound_index = 0
  is_has_more_page = False
  same_sound_last_word=""
  #debug_print("ShowSearch1")        
  #debug_print("ShowSearch2")
  #debug_print("C[-1]:%s" % c[-1])
  #debug_print("C[:-1]:%s" % c[:-1])  
  # 此部分可以修正 V 可以出第二字，還不錯
  # 2017-07-13 Fix when V is last code
  #debug_print("LAST V : %s" % (c[-1]))
  is_need_use_pinyi=False
  #is_need_use_phone=False
  c = ""   
  WORDS_FROM = uclcode["chardefs"]; 
  if kind == None:
    c = my.strtolower(play_ucl_label)
    c = my.trim(c)
    pass
  elif kind == "phone":
    WORDS_FROM = uclcode_phone;
    m = mystts.split_unicode_chrs(str(play_ucl_label))
    
    for i in range(0,my.strlen(m)):    
            
      m[i] = phone_INDEX[phone_DATA.index(m[i])]
    c = my.implode("",m)      
  
  if c[0] == "'" and len(c)>1:
    c=c[1:]
    is_need_use_pinyi=True       
  if c not in WORDS_FROM and c[-1]=='v' and c[:-1] in WORDS_FROM and len(WORDS_FROM[c[:-1]])>=2 :
    #debug_print("Debug V1")
    ucl_find_data = WORDS_FROM[c[:-1]][1]   
    word_label_set_text()
    return True
  elif c not in WORDS_FROM and c[-1]=='r' and c[:-1] in WORDS_FROM and len(WORDS_FROM[c[:-1]])>=3 :
    #debug_print("Debug V1")
    ucl_find_data = WORDS_FROM[c[:-1]][2]   
    word_label_set_text()
    return True
  elif c not in WORDS_FROM and c[-1]=='s' and c[:-1] in WORDS_FROM and len(WORDS_FROM[c[:-1]])>=4 :
    #debug_print("Debug V1")
    ucl_find_data = WORDS_FROM[c[:-1]][3]   
    word_label_set_text()
    return True
  elif c not in WORDS_FROM and c[-1]=='f' and c[:-1] in WORDS_FROM and len(WORDS_FROM[c[:-1]])>=5 :
    #debug_print("Debug V1")
    ucl_find_data = WORDS_FROM[c[:-1]][4]   
    word_label_set_text()
    return True
  elif c in WORDS_FROM:
    #debug_print("Debug V2")
    ucl_find_data = WORDS_FROM[c]
    ucl_find_data_orin_arr = ucl_find_data
    if len(ucl_find_data) > same_sound_max_word:
      #Need page
      ucl_find_data = ucl_find_data_orin_arr[same_sound_index:same_sound_max_word]  
      is_has_more_page = True         
    word_label_set_text()
    return True
  else:
    #debug_print("Debug V3")
    ucl_find_data=[]  
    #play_ucl_label=""  
    #ucl_find_data=[]
    word_label_set_text()
    return False  
  
  #debug_print(find)
  #debug_print("ShowSearch3")
  #debug_print("FIND: [%s] %s" % (play_ucl_label,find))
  #pass
def play_ucl(thekey):
  global type_label
  global play_ucl_label
  global is_need_use_phone
  global pinyi_version  
  global phone_INDEX
  global phone_DATA
  global ucl_find_data
  play_ucl_label = type_label.GetLabel();  
  
  #debug_print(len(play_ucl_label))
  #debug_print(my.strlen(play_ucl_label))
  #my.exit()
  
  if pinyi_version == "0.01" and is_need_use_phone == True and len(str(play_ucl_label)) < 4:
    # 不可以超過5個字 注音查詢模式
    # 這裡是新版的 pinyi
    # issue 165、注音輸入模式，「ㄒㄧㄤ」襄，選不到
    # issue 166、注音輸入模式，輸入的注音順序要防呆、置換
    #這裡是注音模式
    #ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦ
    # From : https://zh.wikipedia.org/wiki/%E6%B3%A8%E9%9F%B3%E7%AC%A6%E8%99%9F
    # 聲母
    phone_level_0 = [u"ㄅ",u"ㄆ",u"ㄇ",u"ㄈ",u"ㄉ",u"ㄊ",u"ㄋ",u"ㄌ",u"ㄍ",u"ㄎ",u"ㄏ",u"ㄐ",u"ㄑ",u"ㄒ",u"ㄓ",u"ㄔ",u"ㄕ",u"ㄖ",u"ㄗ",u"ㄘ",u"ㄙ"]
    # 介音
    phone_level_1 = [u"ㄧ",u"ㄨ",u"ㄩ"]
    # 韻母
    phone_level_2 = [u"ㄚ",u"ㄛ",u"ㄜ",u"ㄝ",u"ㄞ",u"ㄟ",u"ㄠ",u"ㄡ",u"ㄢ",u"ㄣ",u"ㄤ",u"ㄥ",u"ㄦ"]
    # 發音
    phone_level_3 = [u" ",u"ˊ",u"ˇ",u"ˋ",u"˙"]
    # 在此限制注音輸入的順序或代換          
    # debug_print("Debug7 phone char_alreay_keyin: %s" % (str(play_ucl_label)))
    # Debug7 phone char_alreay_keyin: ㄨㄛ

    # 這裡是錯的
    # test = mystts.split_unicode_chrs(play_ucl_label)
    # debug_print(test) # --> ['\xe3', '\x84', '\xa8', '\xe3', '\x84', '\x9b']    

    # 這裡是對的，切開已輸入過的內容
    #test = mystts.split_unicode_chrs(str(play_ucl_label))
    #debug_print(test) # --> [u'\u3128', u'\u311b']

    # 這是使用者輸入的ㄅㄆㄇ
    _data = str(phone_DATA[phone_INDEX.index(thekey)])
    debug_print("Debug 11 _data 使用者輸入 : %s" % (_data))
    debug_print("Debug 11 play_ucl_label 已打的字 : %s" % (str(play_ucl_label)))
    # 在此作防呆    
    # 如果已送出發音查詢，就不能再加字
    if len(ucl_find_data)!=0:
      debug_print(u"Debug 11 ... 如果已送出發音查詢，就不能再加字")
      # 但如果 thekey 是 0~9 當作選字
      debug_print(thekey)
      # 當發音是一聲，才會發生這件事
      if my.is_string_like(str(thekey),mystts.split_unicode_chrs("0123456789")) and int(thekey)<=len(ucl_find_data):
        data = ucl_find_data[int(thekey)]
        senddata(data)
        ucl_find_data = []
        show_sp_to_label(str(data),True)
        #注
        show_phone_to_label(str(data),None)
        # 強制關注音
        is_need_use_phone = False
      return False
    # 不能重複字
    if play_ucl_label != "" and my.is_string_like(play_ucl_label,_data):
      debug_print(u"Debug 11 ... 不能重複字")
      return False
    # 如果字尾已是發音，就不能再加字
    if play_ucl_label != "" and my.in_array(str(play_ucl_label)[-1],phone_level_3):
      debug_print(u"Debug 11 ... 如果字尾已是發音，就不能再加字")
      return False
    # 聲母只能在第一    
    if my.in_array(_data,phone_level_0) and len(str(play_ucl_label))>=1 and my.in_array(str(play_ucl_label)[0:1],phone_level_0):
      debug_print(u"Debug 11 ... 已經有輸入其他聲母了")
      play_ucl_label = str(play_ucl_label)[1:]
      play_ucl_label = "%s%s" % (_data,play_ucl_label)
      ucl_find_data = []
    elif my.in_array(_data,phone_level_0) and len(str(play_ucl_label))>=1 and my.in_array(str(play_ucl_label)[0:1],phone_level_0)==False:
      debug_print(u"Debug 11 ... 有輸入字，但沒有聲母")
      play_ucl_label = "%s%s" % (_data,play_ucl_label)
      ucl_find_data = []
    elif my.in_array(_data,phone_level_1) and len(str(play_ucl_label))>=1 and my.is_string_like(str(play_ucl_label),phone_level_1)==True:
      debug_print(u"Debug 11 ... 輸入介音，但原來已輸入過介音了，置換掉新介音")
      _already_keyin_split = mystts.split_unicode_chrs(str(play_ucl_label))
      for i in range(0,len(_already_keyin_split)):
        if my.is_string_like(_already_keyin_split[i],phone_level_1):
          _already_keyin_split[i]=_data
      play_ucl_label = my.implode("",_already_keyin_split)
      ucl_find_data = []
    elif my.in_array(_data,phone_level_1) and len(str(play_ucl_label))>=1 and my.is_string_like(str(play_ucl_label),phone_level_2)==True:
      debug_print(u"Debug 11 ... 輸入介音，但已輸入過韻母，把韻母往後移")
      play_ucl_label = "%s%s%s" % (str(play_ucl_label)[0:-1],_data,str(play_ucl_label)[-1])
      ucl_find_data = []
    elif my.in_array(_data,phone_level_2) and len(str(play_ucl_label))>=1 and my.is_string_like(str(play_ucl_label),phone_level_2)==True:
      debug_print(u"Debug 11 ... 輸入韻母，但已輸入過韻母，置換韻母")
      _already_keyin_split = mystts.split_unicode_chrs(str(play_ucl_label))
      for i in range(0,len(_already_keyin_split)):
        if my.is_string_like(_already_keyin_split[i],phone_level_2):
          _already_keyin_split[i]=_data
      play_ucl_label = my.implode("",_already_keyin_split)
      ucl_find_data = []
    else:  
      play_ucl_label = "%s%s" % (play_ucl_label,_data)        
      ucl_find_data = []
    # 只有在輸出 發音 ，showOnly 才改成 False
    if my.in_array(_data,phone_level_3):
      type_label_set_text()
    else:
      type_label_set_text(showOnly=True)
    
  elif len(play_ucl_label) < 5:    
    # 不可以超過5個字
    play_ucl_label = "%s%s" % (play_ucl_label,thekey)
    type_label_set_text()
  return True
def senddata(data):
  global play_ucl_label
  global ucl_find_data
  global same_sound_index
  global is_has_more_page
  global same_sound_last_word
  global debug_print
  global f_arr
  global f_big5_arr
  global os_version
  #2019-10-20 增加出字強制選擇
  global DEFAULT_OUTPUT_TYPE
  debug_print("senddata")
  debug_print(str(data))
  #debug_print(data)
  #for i in range(0,len(mTC_TDATA)):
  #  debug_print(mTC_TDATA[i]);
  #my.exit(); 
  #debug_print(mTC_TDATA)
  #簡繁轉換  
  if is_simple():    
    data = mystts.trad2simple(data)
  
  same_sound_index = 0 #回到第零頁
  is_has_more_page = False #回到沒有分頁
  same_sound_last_word=""
  play_ucl_label=""
  ucl_find_data=[]  
  type_label_set_text()  
  
  
  
  hwnd = win32gui.GetForegroundWindow()
  pid = win32process.GetWindowThreadProcessId(hwnd)
  debug_print("Title: -------------------------- ") #批踢踢實業坊 - Google Chrome
  debug_print(win32gui.GetWindowText(hwnd))
  program_title = win32gui.GetWindowText(hwnd)
  
  pp="";
  if len(pid) >=2:
    pp=pid[1]
  else:
    pp=pid[0]
  #debug_print("PP:%s" % (pp))
  debug_print("PP:%s" % (pp))
  p=psutil.Process(pp)
  #debug_print("Send step: 1")
  #debug_print("Send step: 1 p.exe(): %s" % (p.exe()))
  exec_proc = my.strtolower(my.basename(p.exe()))
  #debug_print("Send step: 2")
  #debug_print("ProcessP:%s" % (p))
  #debug_print("Send step: 3")  
  check_kind="0"
  #debug_print("exec_proc: %s" %(exec_proc))
  #debug_print("Send step: 4")
  # 這是貼上模式
  
  # 2023-11-17 Win11 特產 微軟 VBA
  debug_print("XXXXXXXXXXXXXXXD program_title: %s" % (program_title));
  if my.is_string_like(program_title, "Microsoft Visual Basic"):
      debug_print(u"微軟VBA 還在 big5嗎...");
      # 貼上模式，且要貼 big5 ?
      win32clipboard.OpenClipboard() 
      win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常      
      win32clipboard.SetClipboardData(win32con.CF_TEXT, my.utf8tobig5(data))
      win32clipboard.CloseClipboard()
      SendKeysCtypes.SendKeys("^v",pause=0)
      #也許要設delay...
      #time.sleep(0.05)
      #SendKeysCtypes.SendKeys( data.encode('big5'),pause=0)
      return    
  
  # 2023-03-29 Win11 特產  
  # 如果是 windows 11 且使用 notepad.exe 且版本是 11.2302.26.0
  # 如果 notepad 裡使用的字型是 MingLiU 或 MingLiU_HKSCS 就可以正常出字，反之只能用複製貼上出字才能正常@@?
  #debug_print("GGGGGGGG:check_kind  %s " % (check_kind))
  #SendKeysCtypes.SendKeys("字型是")    
  if os_version=="11" and exec_proc == "notepad.exe":
    #且是特定版本才行
    _properties = my.getFileProperties(p.exe())
    '''
    {'FileVersion': '11.2302.26.0', 'FixedFileInfo': {u'FileFlagsMask': 63, u'FileType': 1, u'FileVersionMS': 723198, u'FileVersionLS': 1703936, u'Signature': -17890115, u'FileSubtype': 0, u'FileFlags': 0, u'ProductVersionLS': 1703936, u'FileDate': None, u'ProductVersionMS': 723198, u'FileOS': 4, u'StrucVersion': 65536}, 'StringFileInfo': {'LegalCopyright': None, 'InternalName': None, 'FileVersion': None, 'CompanyName': None, 'PrivateBuild': None, 'LegalTrademarks': None, 'Comments': None, 'ProductName': None, 'SpecialBuild': None, 'ProductVersion': None, 'FileDescription': None, 'OriginalFilename': None}}
    '''
    # 2023-05-15
    # 如果是 windows 11 且使用 notepad.exe 且版本是 11.2302.26.0、11.2303.40.0
    # Issue. 182、Win11 裡的 notepad 需為特定版本：11.23* 才會改成強制複製貼上
    if _properties["FileVersion"] is not None and my.is_string_like(_properties["FileVersion"],"11.23"):
        #debug_print(_properties)
        #debug_print(exec_proc); => notepad.exe
        #debug_print("WTFFFFF win11 notepad need paste");
        orin_clip=""
        #clipID = 0 #win32clipboard.EnumClipboardFormats(0)[0]
        #win32clipboard.OpenClipboard() 
        # 打开系统剪贴板
        

        # 在剪贴板中写入文本数据
        #ctypes.windll.user32.EmptyClipboard()
        #ctypes.windll.user32.SetClipboardData(1, ctypes.c_wchar_p('Hello, clipboard!'))

        # 关闭系统剪贴板
        #ctypes.windll.user32.CloseClipboard()
        
        #try:                        
        #  # Todo 似乎 binary or image copy 無法使用，先這樣吧      
        #  orin_clip = clip.get()      
        #  pass
        #except:
        #  debug_print("error copy")            
        #  pass
        
        
        win32clipboard.OpenClipboard()     
        win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常
        win32clipboard.CloseClipboard() 
        # 176、貼上模式時，如 'pns空白2 的擬，會變成 鏦的問題 (感謝 ym 回報問題)
        #ctypes.windll.user32.OpenClipboard(None)
        #ctypes.windll.user32.SetClipboardData(0, str(data))
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, str(data))       
        win32clipboard.CloseClipboard() 
        SendKeysCtypes.SendKeys("^v",pause=0)
        
        #if orin_clip is not None:
        #  clip.put(orin_clip)
        
        return
               
  for k in f_arr:
    #debug_print("check_kind==f_arr")
    #break;
    k = my.strtolower(k)  
	            
    # 2021-08-08 term.ptt.cc (批踢踢實業坊 - Google Chrome) 改成，強制 paste
    # 2023-11-17 Microsoft VBA (Microsoft Visual Basic for Applications) 上字要改，太舊了
    if my.is_string_like(exec_proc,k) or DEFAULT_OUTPUT_TYPE == "PASTE" or program_title == my.utf8tobig5(u"批踢踢實業坊") or program_title == my.utf8tobig5(u"批踢踢實業坊 - Google Chrome") or program_title == my.utf8tobig5(u"批踢踢實業坊 - Brave") or program_title == my.utf8tobig5(u"批踢踢實業坊 - 個人 - Microsoft? Edge") or program_title == my.utf8tobig5(u"批踢踢實業坊 — Mozilla Firefox") or program_title == my.utf8tobig5(u"批踢踢實業坊 - Opera") or program_title == u"批踢踢實業坊" or program_title == u"批踢踢實業坊 - Google Chrome" or program_title == u"批踢踢實業坊 - Brave" or program_title == u"批踢踢實業坊 - 個人 - Microsoft? Edge" or program_title == u"批踢踢實業坊 — Mozilla Firefox" or program_title == u"批踢踢實業坊 - Opera":
      check_kind="1"            
      #win32clipboard.OpenClipboard()
      orin_clip=""
      #try:
      #  orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
      #except:
      #  pass
      #win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
      #win32clipboard.EmptyClipboard()
      #win32clipboard.CloseClipboard()
      debug_print("The paste mode...")      
      win32clipboard.OpenClipboard() 
      win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常
      # 176、貼上模式時，如 'pns空白2 的擬，會變成 鏦的問題 (感謝 ym 回報問題)
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, str(data))
      win32clipboard.CloseClipboard()
      #https://win32com.goermezer.de/microsoft/windows/controlling-applications-via-sendkeys.html
      #shell.SendKeys("+{INSERT}", 0)
      #2018-04-05 修正 vim 下打中文字的問題
      #debug_print("Debug Oxygen Not Included")
      #SendKeysCtypes.SendKeys("+{INSERT}",pause=0)
      if k == "oxygennotincluded.exe":
        #2019-02-10 修正 缺氧 無法輸入中文的問題
        SendKeysCtypes.SendKeys("^v",pause=0)
      elif k == "iedit_.exe":
        #2019-10-29 修正 PhotoImpact x3 無法輸入中文的問題		
        SendKeysCtypes.SendKeys("^v",pause=0)
      elif k == "iedit_.exe":
        #2019-10-29 修正 PhotoImpact x3 無法輸入中文的問題
        SendKeysCtypes.SendKeys("^v",pause=0)
      else:
        SendKeysCtypes.SendKeys("+{INSERT}",pause=0)
      #SendKeysCtypes.SendKeys("ggggg",pause=0)
      #0xA0 = left shift
      #0x2d = insert            
      #win32api.keybd_event(0x10, 1,0,0)
      #win32api.keybd_event(45, 1,0,0)      
      #time.sleep(.05)            
      #win32api.keybd_event(45,0 ,win32con.KEYEVENTF_KEYUP ,0)
      #win32api.keybd_event(0x10,0 ,win32con.KEYEVENTF_KEYUP ,0)
      
      #win32api.keybd_event(win32con.SHIFT_PRESSED, 0, 0x2d, 0,win32con.KEYEVENTF_KEYUP ,0)
       
      #reload(sys)                                    
      #sys.setdefaultencoding('UNICODE') 
      #SendKeysCtypes.SendKeys("肥".encode("UTF-8"),pause=0)
      #reload(sys)                                    
      #sys.setdefaultencoding('UTF-8')
      #也許要設delay...
      time.sleep(0.05)
      #win32clipboard.OpenClipboard()    
      #win32clipboard.EmptyClipboard()
      #win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      #win32clipboard.CloseClipboard()   
      return      
      break
  for k in f_big5_arr:
    #debug_print("check_kind==f_big5_arr")
    k = my.strtolower(k)
    if my.is_string_like(exec_proc,k) or DEFAULT_OUTPUT_TYPE == "BIG5":
      debug_print("Debug_f_big5_arr")
      #SendKeysCtypes.SendKeys(my.utf8tobig5(data),pause=0)
      check_kind="2"
      win32clipboard.OpenClipboard()
      orin_clip=""
      try:
        orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
      except:
        pass      
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_TEXT, my.utf8tobig5(data))
      win32clipboard.CloseClipboard()
      #之前是用 shell，改用 SendKeysCtypes.SendKeys 看看
      #shell = win32com.client.Dispatch("WScript.Shell")
      #shell.SendKeys("^v", 0)
      SendKeysCtypes.SendKeys("^v")
      time.sleep(0.05)
      win32clipboard.OpenClipboard()    
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      win32clipboard.CloseClipboard()       
      return      
      break
  
  if check_kind=="0":
    #reload(sys)                                    
    #sys.setdefaultencoding('UTF-8')
    #debug_print("CP950")
    #2019-03-02 
    #修正斷行、空白、自定詞庫等功能
    #debug_print("check_kind==0")

    #_str = data.decode("UTF-8") #UTF-8    
    #_str = _str.encode("big5").encode("big5")
    # 這裡是正常出字

    _str = str(data) 
    _str = my.str_replace(" ","{SPACE}",_str)
    _str = my.str_replace("(","{(}",_str)
    _str = my.str_replace(")","{)}",_str)
    _str = my.str_replace("\n","{ENTER}",_str)

    # 164、Neovim(nvim-qt)，輸入「停」會變「\」
    #debug_print("senddata exec_proc: ")
    #debug_print(exec_proc)
    #debug_print("senddata _str: ")
    #debug_print(_str)
    if exec_proc == "nvim-qt.exe" and (my.is_string_like(_str ,"停") or my.is_string_like(_str , "作")):
      win32clipboard.OpenClipboard() 
      win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常
      # 176、貼上模式時，如 'pns空白2 的擬，會變成 鏦的問題 (感謝 ym 回報問題)
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, str(data))
      win32clipboard.CloseClipboard()
      SendKeysCtypes.SendKeys("^r{+}",pause=0)
      return
    
    SendKeysCtypes.SendKeys(_str,pause=0)
    #reload(sys)
    #sys.setdefaultencoding('UTF-8')
  
  #reload(sys)                                    
  #sys.setdefaultencoding('auto')
  #SendKeysCtypes.SendKeys(data.decode("auto"),pause=0)
  
def use_pinyi(data):
  global same_sound_data
  global ucl_find_data
  global same_sound_index
  global same_sound_max_word
  global is_has_more_page
  global debug_print
  global pinyi_version
  finds=""
  range_start = 0;
  if pinyi_version == "0.01":
    range_start = 2
    
  # 這裡是處理同音字的部分
  # finds 是指同音字有哪些字
  # 2022-06-22 klt 版有提到，如「閒 'mou」，應該是找發音接近，而非「見」的資料
  # 深思熟慮後，改成優先找最接近的字排序
  # 排序方法：https://3wa.tw/mypaper/index.php?uid=shadow&mode=view&id=2093
  _mSearch = []          
          
  for i in range(range_start,len(same_sound_data)):
    k = same_sound_data[i]
    if my.is_string_like(k,data):
      #if k.startswith(u'\xe7\x9a\x84'):
      #  k = u[1:]
      if pinyi_version == "0.01":
        m = my.explode(" ",my.trim(k))        
        #finds="%s%s " % (finds,my.implode(" ",m[1:]))
        _mSearch.append({ "index": m[1:].index(data) , "data":my.implode(" ",m[1:])});
      else:
        _mSearch.append({ "index": my.trim(k).index(data) , "data":my.trim(k)});
        #finds="%s%s " % (finds,my.trim(k))
      #debug_print(k)
  
  # 由小至大排序
  _mSearchSorted = sorted(_mSearch,key=lambda gg: gg["index"],reverse=False);
  # merge _mSearchSorted to finds
  for i in range(0, len(_mSearchSorted)):
    finds="%s%s " % (finds,_mSearchSorted[i]["data"])
  
  finds=my.trim(finds);
  finds=my.explode(" ",finds)
  #debug_print(finds)
  #finds=finds[:] 
  #for k in finds:
  #  debug_print(k.encode("UTF-8"))
  # 2021-08-20 如果是 pinyi_version = "0.01" 版，移除第一組
  #if pinyi_version == "0.01":
  #  finds = finds[1:]
  finds = my.array_unique(finds)
  #debug_print("Debug data: %s " % data.encode("UTF-8"))
  debug_print("Debug Finds: %d " % len(finds))
  debug_print("Debug same_sound_index: %d " % same_sound_index)
  debug_print("Debug same_sound_max_word: %d " % same_sound_max_word)  
  maxword = same_sound_index + same_sound_max_word
  # 2020-08-10 103 分頁異常，修正同音字少一字，最後分頁有機會顯示錯誤的問題
  if maxword >= len(finds):
    maxword = len(finds)
    is_has_more_page = False
  else:
    is_has_more_page = True
  ucl_find_data = finds[same_sound_index:maxword]
  debug_print("DEBUG same_sound_index: %d " % same_sound_index)
  same_sound_index=same_sound_index+same_sound_max_word
   
  if same_sound_index>=len(finds):
    same_sound_index=0
  word_label_set_text()
  #finds=my.str_replace(data," ",finds)
  #finds=my.str_replace("  "," ",finds)
#def OnMouseEvent(event):
#  global flag_is_shift_down
#  global flag_is_play_otherkey
#  global hm
#  #if flag_is_shift_down==True:
#    #如果同時按著 shift 時，滑鼠有操作就視窗按別的鍵 ok
#  if event.MessageName == "mouse left down" or event.MessageName == "mouse right down" :
#    #flag_is_shift_down=False
#    flag_is_play_otherkey=True
#    #debug_print(('MessageName: %s' % (event.MessageName)))
#    #debug_print(('Message: %s' % (event.Message))) 
#    #debug_print("Debug event MouseA")
#    #debug_print(flag_is_play_otherkey)
#    #hm.UnhookMouse()
#  return True

# run always thread  
# 2021-08-08 修正 打字音按著鍵會連續音消除
lastKey = None    
def OnKeyboardEvent(event):  
  global last_key # save keyboard last 10 word for ,,,j ,,,x ,,,z...
  global flag_is_win_down
  global flag_is_shift_down
  global flag_is_capslock_down
  global flag_is_play_capslock_otherkey
  global flag_is_ctrl_down
  global flag_is_alt_down
  global flag_is_play_otherkey
  global play_ucl_label
  global ucl_find_data
  global is_need_use_pinyi
  global same_sound_last_word
  global gamemode_btn
  global simple_btn
  global debug_print
  global VERSION
  global f_arr
  global GUI_FONT_16
  global f_pass_app
  global config 
  global m_play_song
  global max_thread___playMusic_counts
  global step_thread___playMusic_counts
  global flag_shift_down_microtime
  global same_sound_index 
  global hm 
  global is_has_more_page
  global same_sound_max_word
  global ucl_find_data_orin_arr
  global lastKey # save keyboard last word for same keyin sound
  global pinyi_version
  global is_need_use_phone
  global pinyi_version
     
  # From : https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
  # 1.26 版，加入打字音的功能
  # 1.37 版，打字音不會因為壓著一直響
  
  try:
    if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1" and event.MessageName == "key down":
      #and len(o_song.keys())!=0 and step_thread___playMusic_counts < max_thread___playMusic_counts:
      if lastKey != event.KeyID:
        lastKey = event.KeyID
        #debug_print("lastKey: ");   
        #debug_print(lastKey);
        play_sound()      
      #thread___playMusic(m_song,int(config['DEFAULT']['KEYBOARD_VOLUME']))
    if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1" and event.MessageName == "key up":
      lastKey = None    
    
    #  playsound.playsound(mp3s[1])
    #debug_print(dir())  
    #try:  
    #debug_print(event)
    '''
    debug_print(('MessageName: %s' % (event.MessageName)))
    debug_print(('Message: %s' % (event.Message)))
    debug_print(('Time: %s' % (event.Time)))
    debug_print(('Window: %s' % (event.Window)))
    debug_print(('WindowName: %s' % (event.WindowName)))
    debug_print(('Ascii: %s, %s' % (event.Ascii, chr(event.Ascii))))
    debug_print(('Key: %s' % (event.Key)))
    debug_print(('KeyID: %s' % (event.KeyID)))
    debug_print(('ScanCode: %s' % (event.ScanCode)))
    debug_print(('Extended: %s' % (event.Extended)))
    debug_print(('Injected: %s' % (event.Injected)))
    debug_print(('Alt: %s' % (event.Alt)))
    debug_print(('Transition: %s' % (event.Transition)))
    debug_print(('IS_UCL %s' % (is_ucl())))
    debug_print('---')
    debug_print(('last_key: %s' % (last_key[-8:])))
    '''
    
    hwnd = win32gui.GetForegroundWindow()  
    pid = win32process.GetWindowThreadProcessId(hwnd)
    pp="";
    if len(pid) >=2:
      pp=pid[1]
    else:
      pp=pid[0]
    #debug_print("PP:%s" % (pp))
    #debug_print("PP:%s" % (pp))
    p=psutil.Process(pp)
    #debug_print("ProcessP:%s" % (p))
    #debug_print("GGGGGGG %s " % (p.exe()))
    
    #debug_print(dir(p))
    exec_proc = my.strtolower(p.exe())
    #debug_print("Process :%s" % (exec_proc))
    #print ("HWND:")
    #print (win32gui.GetWindowText(hwnd))
    
    for k in f_pass_app:
      k = my.strtolower(k)
      if my.is_string_like(exec_proc,k):
        if is_ucl()==True:
          toggle_ucl()
        return True
    # chrome 遠端桌面也不需要肥米
    # 2022-07-12 修正是 遠端桌面，才不需要肥米
    if my.is_string_like(my.strtolower(win32gui.GetWindowText(hwnd)),"- chrome 遠端桌面"):
      if is_ucl()==True:
        toggle_ucl()
      return True
    
    #debug_print("Title: -------------------------- ") #批踢踢實業坊 - Google Chrome
    #debug_print(win32gui.GetWindowText(hwnd))
    #debug_print("XXXXXXXXXXXXXXXXXXXXXXXX");
    #debug_print(pinyi_version);
    #debug_print(is_need_use_phone);
    #debug_print(is_ucl());
    if event.MessageName == "key up":                        
      #if pinyi_version == "0.01" and is_ucl() and my.strtolower(last_key[-2:])=="';":
      #  #debug_print("key up 注:")
      #  #type_label_set_text("注:")        
      #  is_need_use_pinyi = False
      #  is_need_use_phone = True
      #  play_ucl_label=""
      #  ucl_find_data=[]        
      #  #word_label_set_text()
      #  #word_label.SetLabel("注:")
      #  #toAlphaOrNonAlpha() 
      #  return False
      #debug_print("T1");
      #debug_print(word_label_get_text()[0:2]);
      #if pinyi_version == "0.01" and is_ucl() and word_label_get_text()[0:2] == "注:":
      #  return False            
      last_key = last_key + chr(event.Ascii)
      last_key = last_key[-10:]   
      if my.strtolower(last_key[-4:])==",,,c":
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        if is_ucl()==False:
          # change to ucl
          toggle_ucl()        
        simple_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 )))         
        simple_btn.SetLabel("簡")
        simple_btn.Show(True)        
        simple_btn.SetFont(wx.Font(int(GUI_FONT_16["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_16["FONT_WEIGHT"],False,GUI_FONT_16["FONT_NAME"]))  
        #simple_btn.set_justify(gtk.JUSTIFY_CENTER)
      if my.strtolower(last_key[-4:])==",,,t":
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        if is_ucl()==False:
          # change to ucl
          toggle_ucl()        
        simple_btn.SetMinSize((0,int(float(config['DEFAULT']['ZOOM'])*40 )))                 
        simple_btn.SetLabel("")
        simple_btn.Show(False)
        simple_btn.SetFont(wx.Font(int(GUI_FONT_16["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_16["FONT_WEIGHT"],False,GUI_FONT_16["FONT_NAME"]))  
      if my.strtolower(last_key[-7:])==",,,lock":
        last_key = ""
        if gamemode_btn.GetLabel()=="正常模式":
          gamemode_btn_click(gamemode_btn)
      if my.strtolower(last_key[-4:])==",,,-":
        #run small
        #play_ucl_label=""
        #ucl_find_data=[]
        #type_label_set_text()
        #toAlphaOrNonAlpha()
        run_big_small(-0.1)        
      if my.strtolower(last_key[-4:])==",,,+":
        #run big
        #play_ucl_label=""
        #ucl_find_data=[]
        #type_label_set_text()
        #toAlphaOrNonAlpha()
        run_big_small(0.1)
      if my.strtolower(last_key[-4:])==",,,s":
        # run short
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        run_short()
      if my.strtolower(last_key[-4:])==",,,l":
        # run long
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        run_long()
      if my.strtolower(last_key[-4:])==",,,x" and is_ucl():
        # 將框選嘸蝦米的文字，轉成中文字
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        orin_clip=""
        #try:
        #  win32clipboard.OpenClipboard()
        #  orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        #except:
        #  pass
        try:
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
          win32clipboard.EmptyClipboard()
          win32clipboard.CloseClipboard()
        except:
          pass      
        SendKeysCtypes.SendKeys("^C",pause=0.05)
        #也許要設delay...      
        #try:
        win32clipboard.OpenClipboard()
        #try:
        selectData=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        # 參考 http://www.runoob.com/python/python-multithreading.html      
        thread.start_new_thread( thread___x, (selectData, ))
        win32clipboard.CloseClipboard()       
        #except:
        #  pass
        #也許要設delay...
        time.sleep(0.05)
        #try:
        #  win32clipboard.OpenClipboard()    
        #  win32clipboard.EmptyClipboard()
        #  win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
        #  win32clipboard.CloseClipboard()           
        #except:
        #  pass
        return False   
      if my.strtolower(last_key[-4:])==",,,z" and is_ucl():
        # 將框選的文字，轉成嘸蝦米的字
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()                   
        orin_clip=""
        #try:
        #  # 備份原本剪貼簿的內容，有可能文字，圖片之類的吧?
        #  win32clipboard.OpenClipboard()
        #  orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        #except:
        #  pass
        try:
          # 清掉剪貼簿內容
          win32clipboard.OpenClipboard()
          #win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
          win32clipboard.EmptyClipboard()
          win32clipboard.CloseClipboard()
        except:
          pass
        # 利用 ctrl + c 複製目前遊標框選的文字
        SendKeysCtypes.SendKeys("^C",pause=0.05)
        try:
          win32clipboard.OpenClipboard()
          #try:
          #time.sleep(0.05)
          selectData = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT) # 從剪貼簿裡抓出內容
          win32clipboard.CloseClipboard() # 抓完關掉剪貼簿
          #debug_print("#2200 selectData:");
          #debug_print(selectData);
          # 1.47 版，使用 opencc改 修正「簡轉繁」
          # 簡轉繁 # 似乎不能單純用 simple2trad，不然 家 -> 傢，后->後
          # From : https://yanwei-liu.medium.com/python%E8%87%AA%E7%84%B6%E8%AA%9E%E8%A8%80%E8%99%95%E7%90%86-%E5%9B%9B-%E7%B9%81%E7%B0%A1%E8%BD%89%E6%8F%9B%E5%88%A9%E5%99%A8opencc-74021cbc6de3
          # selectData = mystts.simple2trad(selectData) #舊版的 stts 寫法
          
          selectData = myopencc.convert(selectData)
          selectData = word_to_sp(selectData)
          
          #debug_print("#2200 after simple2trad:");
          #debug_print(selectData);
          
          thread.start_new_thread( thread___z, (selectData, ))
        except:
          pass
        #也許要設delay...
        time.sleep(0.05)
        #try:
        #  win32clipboard.OpenClipboard()    
        #  win32clipboard.EmptyClipboard()
        #  win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip) #還原原本剪貼簿內容
        #  win32clipboard.CloseClipboard()
        #except:
        #  pass
        return False             
      if my.strtolower(last_key[-9:])==",,,unlock":          
        last_key = ""               
        if gamemode_btn.GetLabel()=="遊戲模式":
          gamemode_btn_click(gamemode_btn)
      if my.strtolower(last_key[-10:])==",,,version":
        last_key= ""   
        message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
        message.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        message.set_keep_above(True)
        _msg_text = about_uclliu()       
        message.set_markup( _msg_text )
        #toAlphaOrNonAlpha()
        message.show()
        toAlphaOrNonAlpha()  
        response = message.run()
        #toAlphaOrNonAlpha()
        debug_print("Show Version")
        #debug_print(response)
        #debug_print(gtk.ResponseType.BUTTONS_OK)
        if response == -5 or response == -4:
          #message.hide()
          message.destroy()
          #toAlphaOrNonAlpha()  
          play_ucl_label=""
          ucl_find_data=[]
          type_label_set_text()
          toAlphaOrNonAlpha()
          return False      
    #debug_print("LAST_KEY:" + last_key)
    if gamemode_btn.GetLabel()=="遊戲模式":      
      return True    
    
    #thekey = chr(event.Ascii)
    # KeyID = 91 = Lwinkey
    # 2019-07-19
    # 增加，如果是肥模式，且輸入的字>=1以上，按下 esc 鍵，會把字消除  
    if event.MessageName == "key down" and is_ucl() == True and len(play_ucl_label) >=1 and event.Key == "Escape":
      #debug_print("2019-07-19 \n 增加，如果是肥模式，且輸入的字>=1以上，按下 esc 鍵，會把字消除)");
      is_need_use_phone = False
      play_ucl_label = ""
      # issue 167、按 Esc 消除字，但也要同時消除已查到的待選字，如: ucl 打完後，直接按 esc 但按 space 仍會出現肥
      ucl_find_data=[]
      type_label_set_text()
      return False
    if event.MessageName == "key down" and (event.KeyID == 91 or event.KeyID == 92):
      flag_is_win_down = True
      debug_print("Debug event A")
    if event.MessageName == "key up" and (event.KeyID == 91 or event.KeyID == 92):
      flag_is_win_down = False
      debug_print("Debug event B")
    if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift"):
      if flag_is_shift_down==False:
        flag_is_play_otherkey=False
        flag_shift_down_microtime = my.microtime()      
      flag_is_shift_down=True
      debug_print("Debug event CC")
    if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #hm.UnhookMouse()
      if flag_is_shift_down==False:
        flag_is_play_otherkey=False
        flag_shift_down_microtime = my.microtime()      
      flag_is_shift_down=True
      
      #hm.HookMouse()            
      debug_print("Debug event C") 
    debug_print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    debug_print("event.MessageName: %s , event.Key = %s" % (event.MessageName, event.Key))
    # alt is Lmenu and Rmenu
    if (event.MessageName == "key down" or event.MessageName == "key sys down") and (event.Key == "Lmenu" or event.Key == "Rmenu"):
      # Issue 183、按 Ctrl + Alt + Del 後，如果在肥模式，回到視窗沒按 Ctrl 輸入法會失靈
      flag_is_alt_down=True
      debug_print("Debug event Alt A 1")
    if event.MessageName == "key up" and (event.Key == "Lmenu" or event.Key == "Rmenu"):
      # Issue 183、按 Ctrl + Alt + Del 後，如果在肥模式，回到視窗沒按 Ctrl 輸入法會失靈
      flag_is_alt_down=False
      debug_print("Debug event Alt A 2")
      # when key up need return
      return True
    if event.MessageName == "key down" and (event.Key == "Lcontrol" or event.Key == "Rcontrol"):  # and config['DEFAULT']['CTRL_SP'] == "1"
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #2021-03-22 修正英/全時，複製、貼上，按著 Ctrl + 任意鍵 有問題
      #hm.UnhookMouse()        
      flag_is_ctrl_down=True      
      #hm.HookMouse()            
      debug_print("Debug event Ctrl C 1")         
    if event.MessageName == "key up" and (event.Key == "Lcontrol" or event.Key == "Rcontrol"): #  and config['DEFAULT']['CTRL_SP'] == "1"
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #2021-03-22 修正英/全時，複製、貼上，按著 Ctrl + 任意鍵 有問題
      #hm.UnhookMouse()                  
      flag_is_ctrl_down=False      
      #hm.HookMouse()            
      debug_print("Debug event Ctrl C 2")
      return True
    if event.MessageName == "key down" and event.Key == "Capital":
      flag_is_capslock_down=True
      flag_is_play_capslock_otherkey=False
      debug_print("Debug event E")
      return True
    if event.MessageName == "key down" and event.Key != "Capital":
      flag_is_play_capslock_otherkey=True
      # Issue 175、當使用者按 Win+L 登出系統，再次登入 Windows 會無法正常打字
      if flag_is_win_down == True and event.Key == "L":
        # 強制改回 Release Win Key
        debug_print("Issue 175 Force Release Win Key")
        flag_is_win_down = False
        return False      
      debug_print("Debug event F")
      #debug_print("is ucl??")    
      #debug_print(is_ucl())    
      #debug_print("DDDDFFFF event.Key: "+str(event.Key))
      #debug_print("flag_is_shift_down:"+str(flag_is_shift_down))
      #debug_print("flag_is_ctrl_down:"+str(flag_is_ctrl_down))
      #debug_print("flag_is_capslock_down:"+str(flag_is_capslock_down))
      #debug_print("flag_is_play_capslock_otherkey:"+str(flag_is_play_capslock_otherkey))
      #debug_print("flag_is_win_down:"+str(flag_is_win_down))
      #debug_print("flag_is_play_otherkey:"+str(flag_is_play_otherkey))
      #debug_print("flag_isCTRLSPACE:"+str(flag_isCTRLSPACE))        
    if event.MessageName == "key down":
      # Issue 183、按 Ctrl + Alt + Del 後，如果在肥模式，回到視窗沒按 Ctrl 輸入法會失靈      
      #debug_print("Debug event FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
      #debug_print("Debug event.Key = %s" % (event.Key)) # Delete or Decimal or End
      if flag_is_ctrl_down == True and flag_is_alt_down == True and ( event.Key == "Delete" or event.Key == "Decimal" or event.Key == "End"):
        # Release after key finish
        flag_is_ctrl_down = False
        flag_is_alt_down = False
        debug_print("Issue 183 Force Release ctrl alt key")
        # 利用偷按一下 ctrl 修正嗎@@?
        # 羽山發現這樣可以耶，笑死
        
        SendKeysCtypes.SendKeys("^",pause=0) # 左邊的 ctrl 按一下
        # From : https://github.com/vsajip/pywinauto/blob/master/pywinauto/SendKeysCtypes.py
        SendKeysCtypes.SendKeys("{VK_RCONTROL}",pause=0); # 右邊的 ctrl 也按一下

        flag_is_ctrl_down = False
        flag_is_alt_down = False
        return False
    if event.MessageName == "key up" and event.Key == "Capital":
      flag_is_capslock_down=False
      flag_is_play_capslock_otherkey=False
      debug_print("Debug event E")
    if event.MessageName == "key down" and (event.Key != "Lshift" and event.Key != "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      debug_print("Debug event D")
      flag_is_play_otherkey=True   
    debug_print("Debug event F1")
    if flag_is_capslock_down == True and flag_is_play_capslock_otherkey == True:
      # 2019-03-06 增加，如果是 肥 模式，且輸入字是 backspace 且框有字根，就跳過這個 True
      if event.Key == "Back" and is_ucl()==True and len(play_ucl_label) >= 1:
        debug_print("Debug 2019-03-06 CapsLock + backspace")
        pass
      else:  
        return True
    if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
      flag_is_shift_down=False
    debug_print("Debug event F2")           
    if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      debug_print("Debug event G")
      debug_print("event.MessageName:"+event.MessageName)
      debug_print("event.Ascii:"+str(event.Ascii))
      debug_print("event.KeyID:"+str(event.KeyID))
      debug_print("flag_is_play_otherkey:"+str(flag_is_play_otherkey))
      debug_print("flag_is_shift_down:"+str(flag_is_shift_down))        
      debug_print("flag_is_capslock_down:"+str(flag_is_capslock_down))
      debug_print("flag_is_play_capslock_otherkey:"+str(flag_is_play_capslock_otherkey))
      flag_is_shift_down=False
      #hm.UnhookMouse()
      debug_print("Press shift")
      
      #2021-03-20 如果 microtime() - flag_shift_down_microtime>=500 flag_is_play_otherkey = true
      st = my.microtime() - flag_shift_down_microtime
      debug_print("st: %d " % (st))
      if st>=500:
         flag_is_play_otherkey = True
      # 不可是右邊的2、4、6、8      
      #toAlphaOrNonAlpha()
      if flag_is_play_otherkey==False and (event.Ascii > 40 or event.Ascii < 37) :
        toggle_ucl()
        debug_print("Debug15")        
        debug_print("Debug14")
  
      #toAlphaOrNonAlpha()
      return True
    if event.MessageName == "key down" and event.Ascii==32 and flag_is_shift_down==True:
      # Press shift and space
      # switch 半/全
      # 2021-07-05 如果有下一頁， shift + space 改成換下頁哦
      if int(config['DEFAULT']['ENABLE_HALF_FULL']) == 1:
          if my.is_string_like(word_label.GetLabel(),"...") == True:
            debug_print("FFFFFFFIND WORDS...")
            debug_print("ucl_find_data_orin_arr")
            #debug_print(ucl_find_data_orin_arr)        
            debug_print("ucl_find_data")
            #debug_print(ucl_find_data)
            debug_print("same_sound_index")
            #debug_print(same_sound_index)        
            same_sound_index = same_sound_index+same_sound_max_word
            if same_sound_index > len(ucl_find_data_orin_arr)-1:
              same_sound_index = 0  
            maxword = same_sound_index + same_sound_max_word
            if maxword > len(ucl_find_data_orin_arr)-1:
               maxword = len(ucl_find_data_orin_arr)           
            ucl_find_data = ucl_find_data_orin_arr[same_sound_index:maxword]  
            debug_print("after ucl_find_data")
            #debug_print(ucl_find_data)                               
            word_label_set_text()        
            return False                     
          else:
            hf_btn_click(hf_btn)
            flag_is_play_otherkey=True
            #2021-08-08 修正 shift+space shift 按著，空白連按，無法連續切換
            #flag_is_shift_down=False    
            debug_print("Debug13")
            return False         
    debug_print("Debug event F3")    
    debug_print("Debug event is_ucl: %s" % is_ucl())  
    if is_ucl():
      #debug_print("is ucl")    
      if event.MessageName == "key down" and flag_is_win_down == True : # win key
        debug_print("Debug event F4")    
        return True
      #2018-05-05要考慮右邊數字鍵的 .
      #2021-08-31這裡是正常送字的部分
      #debug_print("XXXXXXXXXXXXD")
      #debug_print((phone_INDEX.index(chr(event.Ascii))>=0))
      #if event.MessageName == "key down" and pinyi_version == "0.01" and is_need_use_phone == False and event.Ascii==59 and c[0]=="'": # '; 的 ;
      if event.MessageName == "key up" and is_need_use_phone == False and pinyi_version == "0.01" and is_ucl() and my.strtolower(last_key[-2:])=="';":
        debug_print("Debug221_OK")
        is_need_use_pinyi = False
        is_need_use_phone = True
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text("注:")
        toAlphaOrNonAlpha()
        return False            
      if event.MessageName == "key down" and ( event.Ascii == 8 ): # ←      
        if my.strlen(str(play_ucl_label)) <= 0:                    
          play_ucl_label=""
          play_ucl("")
          debug_print("Debug6")
          return True
        else:
          play_ucl_label = str(play_ucl_label)[:-1]
          if is_need_use_phone == True:
            # 這裡是指，按了注音，又按 Backspace 的事件
            # 要清掉 word_label
            type_label_set_text("注:",showOnly=True)            
            ucl_find_data=[]
            return False
          type_label_set_text()
          debug_print("Debug5")        
          return False
      # 2021-08-31 orin 0~9        
      # 是、非注音模式時   
      debug_print("Debug event F5")
      if event.MessageName == "key down" and ( event.Ascii>=48 and event.Ascii <=57) or (event.Key=="Decimal" and event.Ascii==46) : #0~9 .
      
        LAST_CODE = "";
        _is_sound_kick = False
        if is_need_use_phone == True and pinyi_version == "0.01":                              
          # From : https://stackoverflow.com/questions/4978787/how-to-split-a-string-into-a-list-of-characters-in-python  
          LAST_CODE = list(phone_to_en_num(type_label.GetLabel()))
          _s = [" ","6","3","4","7"]
          #debug_print(_s)
          #debug_print(LAST_CODE)
          for i in range(0, len(_s)):
            if _s[i] in LAST_CODE:
              _is_sound_kick = True 
         
        # Fix by Benson9954029
        # Issue 51
        # 如 h backspace v 出現 要
        # 如 v backspace 0 出現 要
        #debug_print("Test v backspace 0 Start")
        if is_need_use_phone == False and len(ucl_find_data)>=1 and int(chr(event.Ascii)) < len(ucl_find_data) and len(word_label.GetLabel()) > 0:
          #debug_print("Test v backspace 0 End")
          # send data        
          data = ucl_find_data[int(chr(event.Ascii))]
          #debug_print(ucl_find_data)
          
          senddata(data)
          show_sp_to_label(str(data),None)
          #注
          show_phone_to_label(str(data),None)
          #debug_print(data)
          #快選用的   
          debug_print("Debug12")
          return False
        elif pinyi_version == "0.01" and is_need_use_phone == True and len(ucl_find_data)>=1 and int(chr(event.Ascii)) < len(ucl_find_data) and _is_sound_kick == True:
          #注音模式要多檢查使用者是不是已打了 space、二聲、三聲、四聲、輕音才出字
          # send data        
          data = ucl_find_data[int(chr(event.Ascii))]
          #debug_print(ucl_find_data)
          
          senddata(data)
          # 這裡要強制 show_sp
          show_sp_to_label(str(data),True)
          #注
          show_phone_to_label(str(data),None)
          
          #debug_print(data)
          #快選用的   
          debug_print("Debug12 phone")
          # 2021-08-31 強制關注音
          is_need_use_phone = False
          return False 
        else:
          if len(event.Key) == 1 and is_hf(None)==False:
            #k = widen(event.Key)
            kac = event.Ascii          
            k = widen(chr(kac))
            #debug_print("event.Key to Full:%s %s" % (event.Key,k))
            senddata(k)
            debug_print("Debug11")
            return False
          
          debug_print("Debug10")
          #2017-10-24要考慮右邊數字鍵的狀況
          #2018-05-05要考慮右邊數字鍵的 .
          # event.Ascii==46 or (event.Key=="Decimal" and event.Ascii==46)
          # 先出小點好了
          if is_need_use_phone == False:
            if is_hf(None)==False and ( event.Ascii==49 or event.Ascii==50 or event.Ascii==51 or event.Ascii==52 or event.Ascii==53 or event.Ascii==54 or event.Ascii==55 or event.Ascii==56 or event.Ascii==57 or event.Ascii==47 or event.Ascii==42 or event.Ascii==45 or event.Ascii==43 or event.Ascii==48):
              kac = event.Ascii        
              k = widen(chr(kac))
              #if event.Ascii==46:
              #  senddata("a")
              #else:
              senddata(k)
              debug_print("Debug100")
              return False
            else:  
              return True 
      debug_print("Debug event F6")         
      debug_print("F61 is_need_use_phone: %s" % (is_need_use_phone))
      debug_print("F61 event.Ascii: %s" % (event.Ascii))
      debug_print("F61 event.KeyID: %s" % (event.KeyID))
      debug_print("F61 event.Key: %s" % (event.Key))
      debug_print(('MessageName: %s' % (event.MessageName)))
      debug_print(('Message: %s' % (event.Message)))
      debug_print(('Time: %s' % (event.Time)))
      debug_print(('Window: %s' % (event.Window)))
      debug_print(('WindowName: %s' % (event.WindowName)))
      debug_print(('Ascii: %s, %s' % (event.Ascii, chr(event.Ascii))))
      debug_print(('Key: %s' % (event.Key)))
      debug_print(('KeyID: %s' % (event.KeyID)))
      debug_print(('ScanCode: %s' % (event.ScanCode)))
      debug_print(('Extended: %s' % (event.Extended)))
      debug_print(('Injected: %s' % (event.Injected)))
      debug_print(('Alt: %s' % (event.Alt)))
      debug_print(('Transition: %s' % (event.Transition)))      
      '''
        F61 is_need_use_phone: False
        F61 event.Ascii: 0 # 這裡有 bug 參考：https://stackoverflow.com/questions/41652232/pyhook-giving-wrong-ascii-values
        用 KeyID 取代 Ascii 似乎較好!?
        F61 event.KeyID: 65
        F61 event.Key: A
            ASCII keyID
        a      97    65
        z     122    90
        A      65    65
        Z      90    90
      '''
      # issue 183、按 Ctrl + Alt + Del 後，如果在肥模式，回到視窗沒按 Ctrl 輸入法會失靈
      # 羽山發現當按下 Ctrl+ Alt + Del 後，回到畫面，event.Ascii 會變成 0
      if is_need_use_phone == False and event.MessageName == "key down" and ( (event.Ascii>=65 and event.Ascii <=90) or (event.Ascii>=97 and event.Ascii <=122) or event.Ascii==44 or event.Ascii==46 or event.Ascii==39 or event.Ascii==91 or event.Ascii==93):      
        # 這裡是肥米吃到字的地方
        debug_print("Debug event F61")
        flag_is_play_otherkey=True
        if flag_is_shift_down==True:
          if len(event.Key) == 1 and is_hf(None)==False:
            #k = widen(event.Key)
            kac = event.Ascii
            if kac>=65 and kac<=90:
              kac=kac+32
            else:
              kac=kac-32
            k = widen(chr(kac))
            debug_print("285 event.Key to Full:%s %s" % (event.Key,k))
            senddata(k)
            debug_print("Debug9")
            return False
          debug_print("Debug8")
          return True                  
        else:
          # Play ucl
          #debug_print("Play UCL")
          #debug_print(thekey)
          play_ucl(chr(event.Ascii))
          debug_print("Debug7")
          return False          
      # 2021-08-31
      # normal and phone
      debug_print("Debug event F7")
      if pinyi_version == "0.01" and is_need_use_phone == True and event.MessageName == "key down" and ( (event.Ascii>=65 and event.Ascii <=90) or (event.Ascii>=97 and event.Ascii <=122) or (event.Ascii>=48 and event.Ascii <=57) or event.Ascii==44 or event.Ascii==46 or event.Ascii==47 or event.Ascii==59 or event.Ascii==45):
        # 這裡應該是同時按著SHIFT的部分
        flag_is_play_otherkey=True
        if flag_is_shift_down==True:
          if len(event.Key) == 1 and is_hf(None)==False:
            #k = widen(event.Key)
            kac = event.Ascii
            if kac>=65 and kac<=90:
              kac=kac+32
            else:
              kac=kac-32
            k = widen(chr(kac))
            debug_print("phone 2855 event.Key to Full:%s %s" % (event.Key,k))
            senddata(k)
            debug_print("Debug9 phone")
            return False
          debug_print("Debug8 phone")
          return True                  
        else:
          # Play ucl
          #debug_print("Play UCL")
          #debug_print(thekey)          
          play_ucl(chr(event.Ascii))
          debug_print("Debug7 phone")
          return False
      debug_print("Debug event F8")
      if event.MessageName == "key down" and event.Key=="Space" and config['DEFAULT']['CTRL_SP']=="1": # check ctrl + space
          if flag_is_ctrl_down == True:
            toggle_ucl()
            return False
      debug_print("Debug event F9")
      if event.MessageName == "key down" and event.Key=="Space": #空白
        # Space                          
        #表裡面有字才會出
        if len(ucl_find_data)>=1 and len(word_label.GetLabel())>0:        
          #丟出第一個字                
          text = ucl_find_data[0]
          if same_sound_last_word=="":
            same_sound_last_word=text
          #] my.utf8tobig5("好的")          
          if is_need_use_pinyi==True:
            #使用同音字
            debug_print("Debug use pinyi")
            use_pinyi(same_sound_last_word)
          else:
            #在這作，如果有分頁，要切換分頁
            #2021-07-05            
            finds = my.array_unique(ucl_find_data)
            #debug_print("Debug data: %s " % data.encode("UTF-8"))
            debug_print("Debug Finds: %d " % len(finds))
            debug_print("Debug same_sound_index: %d " % same_sound_index)
            debug_print("Debug same_sound_max_word: %d " % same_sound_max_word)  
            maxword = same_sound_index + same_sound_max_word
            # 2020-08-10 103 分頁異常，修正同音字少一字，最後分頁有機會顯示錯誤的問題
            if maxword >= len(finds):
              maxword = len(finds)
              is_has_more_page = False
            else:
              is_has_more_page = True
            ucl_find_data = finds[same_sound_index:maxword]
            debug_print("DEBUG same_sound_index: %d " % same_sound_index)
            same_sound_index=same_sound_index+same_sound_max_word
             
            if same_sound_index>=len(finds):
              same_sound_index=0
           
            senddata(text)   
            #2021-07-22 補 sp 出字
            show_sp_to_label(text,None)
            #注
            show_phone_to_label(text,None)                         
          debug_print("Debug4")
          # 2021-08-31 這裡是按下 sp 出字，一樣把注音關了
          if is_need_use_phone == True and pinyi_version == "0.01":
            is_need_use_phone = False
            show_sp_to_label(text,True)
            #注
            show_phone_to_label(text,None)          
          return False 
        elif len(ucl_find_data)==0 and len(play_ucl_label)!=0:
          debug_print("Debug phone 11 is_need_use_phone: %s " % (is_need_use_phone))
          debug_print("Debug phone 11 event.Ascii: %s " % (event.Ascii))
          if is_need_use_phone == True and event.Ascii == 32:
            # 這裡是指，注音模式下，有打字，按了空音
            debug_print("Debug phone 11")
            #play_ucl(chr(event.Ascii))
            # 加入發音            
            type_label_set_text()
            return False

          #無此字根時，按到空白鍵
          debug_print("Debug16")
          play_ucl_label=""
          ucl_find_data=[]
          type_label_set_text()
          return False 
        else:
          #沒字時直接出空白
          debug_print("Debug1")
          if is_hf(None)==False:        
            kac = event.Ascii        
            k = widen(chr(kac))
            senddata(k)
            debug_print("Debug23")
            return False
          else:
            return True
      elif event.MessageName == "key down" and ( event.Ascii==58 or event.Ascii==59 or event.Ascii==123 or event.Ascii==125 or event.Ascii==40 or event.Ascii==41 or event.Ascii==43 or event.Ascii==126 or event.Ascii==33 or event.Ascii==64 or event.Ascii==35 or event.Ascii==36 or event.Ascii==37 or event.Ascii==94 or event.Ascii==38 or event.Ascii==42 or event.Ascii==95 or event.Ascii==60 or event.Ascii==62 or event.Ascii==63 or event.Ascii==34 or event.Ascii==124 or event.Ascii==47 or event.Ascii==45) : # : ;｛｝（）＋～！＠＃＄％＾＆＊＿＜＞？＂｜／－
        debug_print("Debug event F12")
        #debug_print("Debug for '; ")
        #debug_print("event.Ascii")
        #debug_print(event.Ascii)
        #debug_print(is_need_use_pinyi)
        c = my.strtolower(play_ucl_label)
        c = my.trim(c)
        #修正 肥/全 時，按分號、冒號只出半型的問題
        if is_hf(None)==False:        
          kac = event.Ascii        
          k = widen(chr(kac))
          senddata(k)
          debug_print("Debug22")
          return False
        else:          
          #debug_print(is_need_use_phone)
          if type_label.GetLabel()=="'" and pinyi_version == "0.01":
            debug_print("Debug22OK phone")
            return False
          debug_print("Debug22OK")
          return True     
      else:
        debug_print("Debug event F11")
        debug_print("Debug event F11 flag_is_ctrl_down: %s" % (flag_is_ctrl_down))
        debug_print("Debug event F11 flag_is_alt_down: %s" % (flag_is_alt_down))
        debug_print("Debug event F11 flag_is_shift_down: %s" % (flag_is_shift_down))
        debug_print("Debug event F11 flag_is_play_otherkey: %s" % (flag_is_play_otherkey))
        return True            
      debug_print("Debug event F10")  
    else: # not is_ucl()
      debug_print("DDDDDDDDD: event.Key: " + event.Key + "\nDDDDDDDDD: event.KeyID: " + str(event.KeyID) + "\nDDDDDDDDD: event.MessageName: " +  event.MessageName )
      debug_print("flag_is_shift_down:"+str(flag_is_shift_down))
      debug_print("flag_is_ctrl_down:"+str(flag_is_ctrl_down))
      debug_print("Debug3")  
      debug_print(event.KeyID)
      # 2021-12-02 如果在英/全 模式，按 numlock、scroll lock 無法穿透的問題
      if event.Key == "Numlock" or event.Key == "Scroll":
        return True 
      
      # 2018-03-27 此部分修正「英/全」時，按Ctrl A 無效的問題，或ctrl+esc等問題
      # 修正enter、winkey 在「英/全」的狀況
      if event.MessageName == "key down" and event.KeyID == 13:
        return True
      if event.MessageName == "key down" and ( event.KeyID == 91 or event.KeyID == 92): #winkey
        flag_is_win_down=True
        return True
      # 修正  在「英/全」的狀況，按下 esc (231 + 27 ) 無效的問題
      if event.MessageName == "key down" and ( event.KeyID == 231 or event.KeyID == 27):
        flag_is_win_down=False
        debug_print("Fix 23+27")
        return True                
      if event.MessageName == "key down" and flag_is_win_down == True : # win key
        flag_is_win_down=False
        return True          
      #if event.MessageName == "key down" and ( event.KeyID == 231 or event.KeyID == 162 or event.KeyID == 163):
      #  flag_is_ctrl_down=True
      #  debug_print("Ctrl key")
      #  return True
      #if flag_is_ctrl_down == True:
      #  flag_is_ctrl_down=False
      #  return True       
      if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift"):      
        flag_is_shift_down=True
        flag_is_play_otherkey=False      
        debug_print("Debug331")                
      if event.MessageName == "key down" and (event.Key != "Lshift" and event.Key != "Rshift"): 
        flag_is_play_otherkey=True                                                                               
        debug_print("Debug332")                
      if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
        debug_print("Debug333")
        #shift
        flag_is_shift_down=False
        debug_print("Press shift")
      if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
        if flag_is_play_otherkey==False:
          toggle_ucl()
          debug_print("Debug315")    
        debug_print("Debug314")
        return True
                
      if event.MessageName == "key down" and event.Key=="Space" and config['DEFAULT']['CTRL_SP']=="1": # check ctrl + space
        if flag_is_ctrl_down == True:
          toggle_ucl()
          return False
      #2021-03-22 修正 英/全 模式下，按 CTRL + 任意鍵，也是穿透的問題
      if is_hf(None)==False and event.MessageName == "key down" and flag_is_ctrl_down == True:
        return True        
      #if event.MessageName == "key up" and len(event.Key) == 1 and is_hf(None)==False:
      #  k = widen(event.Key)
      #  debug_print("335 event.Key to Full:%s %s" % (event.Key,k))
      #  senddata(k)
      #  return False
      #if len(event.Key) == 1 and is_hf(None)==False and event.KeyID !=0 and event.KeyID !=145 and event.KeyID !=162:
      #  k = widen(event.Key)      
      #  senddata(k) 
      debug_print("Debug3: %s" % (event.Transition))
      if event.KeyID==8 or event.KeyID==20 or event.KeyID==45 or event.KeyID==46 or event.KeyID==36 or event.KeyID==33 or event.KeyID==34 or event.KeyID==35 or event.KeyID==160 or event.KeyID==161 or event.KeyID==9 or event.KeyID == 37 or event.KeyID == 38 or event.KeyID == 39 or event.KeyID == 40 or event.KeyID == 231 or event.KeyID == 162 or event.KeyID == 163: #↑←→↓
        return True
      if event.MessageName == "key down" and len( str(chr(event.Ascii)) ) == 1 and is_hf(None)==False and event.Injected == 0 :
        k = widen( str(chr(event.Ascii)) )
        #debug_print("ｋｋｋｋｋｋｋｋｋｋｋｋｋｋｋK:%s" % k)
        senddata(k)
        return False
      return True    
  except Exception as e:
    # 理論上不會發生，也不該發生
    debug_print("KeyPressed")
    debug_print(e)
    # 這才能知道錯哪一行
    import traceback
    traceback_info = traceback.format_exc()
    print(f"Exception occurred: {e}")
    print(f"Traceback:\n{traceback_info}")
    return True
      
#程式主流程
#功能說明


# create a hook manager
hm = pyWinhook.HookManager()
#hm.UnhookMouse();
# watch for all mouse events
hm.KeyAll = OnKeyboardEvent
#debug_print(dir(hm))
# set the hook
hm.HookKeyboard()
# wait forever

# watch for all mouse events
# 2021-03-19 改成只Hook MouseAllButtons，MouseAll 好像會造成lag
# From : http://pyhook.sourceforge.net/doc_1.5.0/
#hm.MouseAll = OnMouseEvent
#hm.MouseAllButtons = OnMouseEvent
# set the hook
# 改成按到 shift 才 hook
#hm.HookMouse()



# 將窗口設置爲可拖動
is_drag = False
def on_left_down_move(event):
    global win
    global is_drag
    #win.CaptureMouse()
    win.start_pos = event.GetPosition()
    #print(win.start_pos)
    #event.Skip()
    is_drag = False
    
def on_left_up_move(event):
    global win
    global is_drag    
    if is_drag==True:
        if win.HasCapture():
            win.ReleaseMouse()
    else:
        # trigger click
        #debug_print(event.GetId())
        #debug_print(dir(event))
        # 獲取觸發事件的按鈕物件
        button = event.GetEventObject()
        btnName = button.GetName()
        debug_print(btnName)
        if btnName == "肥英按鈕":
            uclen_btn_click(uclen_btn)
        elif btnName == "半全按鈕":
            hf_btn_click(hf_btn)    
        elif btnName == "正常遊戲按鈕":
            gamemode_btn_click(gamemode_btn)
        elif btnName == "Ｘ按鈕":
            x_btn_click(x_btn)     
    if win.HasCapture():
        win.ReleaseMouse()
def on_mouse_motion_move(event):
    global win
    global is_drag
    if event.Dragging() and event.LeftIsDown():            
        delta = event.GetPosition() - win.start_pos
        win.Move(win.GetPosition() + delta)
        is_drag = True
    pass
 

#win.SetSize((int(float(config['DEFAULT']['ZOOM'])*840) , int(float(config['DEFAULT']['ZOOM'])*40 )))

#win.SetWindowStyle(wx.RESIZE_BORDER)



#win.move(screen_width-700,int(screen_height*0.87))
win.Move( int(config["DEFAULT"]["X"]) , int(config["DEFAULT"]["Y"]))
#always on top
win.SetWindowStyle(wx.STAY_ON_TOP)
#win.set_keep_below(False)
win.SetTransparent(0)
#win.SetOpacity(0)
#win.set_skip_taskbar_hint(False)  
#win.set_skip_pager_hint(False)
#win.set_decorated(False)
#win.set_accept_focus(False)
#win.SetFocusIgnoringChildren()
#win.set_icon_name(None)
#win.SetIcon(wx.Icon(name=""))

#win.add_events( gdk.BUTTON_PRESS_MASK)
#win.Bind('button-press-event', winclicked)


#vbox = gtk.VBox(False)
vbox = wx.BoxSizer(wx.VERTICAL)

#hbox=gtk.HBox()
hbox = wx.BoxSizer(wx.HORIZONTAL)
#vbox.pack_start(hbox, False)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND )

uclen_btn=wx.Button(win, label="肥",name="肥英按鈕")
uclen_btn.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))
#uclen_btn.SetLabelVerticalAlignment(wx.VERTICAL_ALIGNMENT_CENTER)
#uclen_btn.connect("clicked",uclen_btn_click)
# 肥的點擊事件

uclen_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
hbox.Add(uclen_btn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL)

uclen_btn.Bind(wx.EVT_LEFT_DOWN, on_left_down_move)
uclen_btn.Bind(wx.EVT_LEFT_UP, on_left_up_move)
uclen_btn.Bind(wx.EVT_MOTION, on_mouse_motion_move)
#uclen_btn.Bind(wx.EVT_BUTTON, uclen_btn_click)

hf_btn=wx.Button(win, label="半",name="半全按鈕")
hf_btn.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))
#hf_btn.SetLabelVerticalAlignment(wx.VERTICAL_ALIGNMENT_CENTER)
#hf_btn.Bind(wx.EVT_BUTTON, hf_btn_click)

hf_btn.Bind(wx.EVT_LEFT_DOWN, on_left_down_move)
hf_btn.Bind(wx.EVT_LEFT_UP, on_left_up_move)
hf_btn.Bind(wx.EVT_MOTION, on_mouse_motion_move)

hf_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
hbox.Add(hf_btn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL)

type_label = wx.TextCtrl(win, value="",style=wx.TE_READONLY)
type_label.SetFont(wx.Font(int(GUI_FONT_22["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_22["FONT_WEIGHT"],False,GUI_FONT_22["FONT_NAME"]))
#type_label.SetLabelVerticalAlignment(wx.VERTICAL_ALIGNMENT_CENTER)
#type_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
type_label.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
type_label.SetBackgroundColour(wx.Colour(222, 222, 222))
type_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*100) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
#type_label.set_alignment(xalign=0.1, yalign=0.5) 
#sizer = wx.BoxSizer()
#sizer.Add(type_label, 0, wx.ALIGN_CENTER_VERTICAL)
#type_label_vbox = wx.BoxSizer(wx.VERTICAL)
#type_label_vbox.Add(type_label, flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL , border=10)
hbox.Add(type_label, 50, wx.RIGHT | wx.ALIGN_BOTTOM)
#hbox.Add(sizer, 0 , wx.LEFT | wx.ALIGN_BOTTOM )

type_label.Bind(wx.EVT_LEFT_DOWN, on_left_down_move)
type_label.Bind(wx.EVT_LEFT_UP, on_left_up_move)
type_label.Bind(wx.EVT_MOTION, on_mouse_motion_move)


word_label=wx.TextCtrl(win, value="",style=wx.TE_READONLY)
word_label.SetFont(wx.Font(int(GUI_FONT_20["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_20["FONT_WEIGHT"],False,GUI_FONT_20["FONT_NAME"]))
word_label.SetBackgroundColour(wx.Colour(222, 222, 222))
word_label.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
word_label.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*350) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
#word_label.SetLabelVerticalAlignment(wx.VERTICAL_ALIGNMENT_CENTER)
#word_label.set_alignment(xalign=0.05, yalign=0.5)
hbox.Add(word_label, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL)

word_label.Bind(wx.EVT_LEFT_DOWN, on_left_down_move)
word_label.Bind(wx.EVT_LEFT_UP, on_left_up_move)
word_label.Bind(wx.EVT_MOTION, on_mouse_motion_move)

# 加一個簡繁互換的
simple_btn=wx.Button(win, label="",name="簡繁按鈕")
simple_btn.SetMinSize((0 ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
simple_btn.SetFont(wx.Font(int(GUI_FONT_16["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_16["FONT_WEIGHT"],False,GUI_FONT_16["FONT_NAME"]))
#simple_btn.SetLabelVerticalAlignment(wx.VERTICAL_ALIGNMENT_CENTER)
simple_btn.Bind(wx.EVT_LEFT_DOWN, on_left_down_move)
simple_btn.Bind(wx.EVT_LEFT_UP, on_left_up_move)
simple_btn.Bind(wx.EVT_MOTION, on_mouse_motion_move)



#simple_label.set_justify(gtk.JUSTIFY_CENTER)
#simple_label.set_alignment(xalign=0.05, yalign=0.5)
hbox.Add(simple_btn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL)


gamemode_btn=wx.Button(win, label="正常模式",name="正常遊戲按鈕")
gamemode_btn.SetFont(wx.Font(int(GUI_FONT_12["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_12["FONT_WEIGHT"],False,GUI_FONT_12["FONT_NAME"]))
#gamemode_btn.Bind(wx.EVT_BUTTON, gamemode_btn_click)

gamemode_btn.Bind(wx.EVT_LEFT_DOWN, on_left_down_move)
gamemode_btn.Bind(wx.EVT_LEFT_UP, on_left_up_move)
gamemode_btn.Bind(wx.EVT_MOTION, on_mouse_motion_move)

gamemode_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*80) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
#gamemode_btn.SetLabelVerticalAlignment(wx.VERTICAL_ALIGNMENT_CENTER)
hbox.Add(gamemode_btn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL)

x_btn=wx.Button(win, label="╳",name="Ｘ按鈕")
x_btn.SetFont(wx.Font(int(GUI_FONT_14["FONT_SIZE"]), wx.DEFAULT, wx.NORMAL, GUI_FONT_14["FONT_WEIGHT"],False,GUI_FONT_14["FONT_NAME"]))
x_btn.SetMinSize((int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))) 
#x_btn.SetLabelVerticalAlignment(wx.VERTICAL_ALIGNMENT_CENTER)
#x_btn.Bind(wx.EVT_BUTTON, x_btn_click)
x_btn.Bind(wx.EVT_LEFT_DOWN, on_left_down_move)
x_btn.Bind(wx.EVT_LEFT_UP, on_left_up_move)
x_btn.Bind(wx.EVT_MOTION, on_mouse_motion_move)

hbox.Add(x_btn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL)


win.SetSizer(vbox)
win.SetSizerAndFit(vbox)
# 2019-10-20 加入 trayicon
def message(data=None):
  "Function to display messages to the user."
  
  msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL,
    gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
  msg.run()
  msg.destroy()


class TrayIcon():
    systray = ""
    def __init__(self):
      global VERSION
      global PWD
      #global UCL_PIC_BASE64
      global my
      global ICON_PATH
      # base64.b64decode
      # From : https://sourceforge.net/p/matplotlib/mailman/message/20449481/
      raw_data = base64.b64decode(str(UCL_PIC_BASE64))
      #if my.is_file(ICON_PATH) == False:
      #2021-08-11
      #生小圖，等會載入完就移除
      debug_print(ICON_PATH)
      try:
        my.file_put_contents(ICON_PATH,raw_data,False)      
      except e:      
        pass
      self.reload_tray()            
    def reload_tray(self):
      global config
      global ICON_PATH
      #global NOW_VOLUME
      global DEFAULT_OUTPUT_TYPE
      global UCL_PIC_BASE64           
      menu_options = (
          (my18.auto("1.關於肥米輸入法"), None, [self.m_about] ),          
        )
      if gamemode_btn.GetLabel()=="正常模式":
        menu_options = menu_options + ((
          (my18.auto("2.切換至「遊戲模式」"), None, [self.m_game_switch] ),          
        ))                
      else:
        menu_options = menu_options + ((
          (my18.auto("2.切換至「正常模式」"), None, [self.m_game_switch] ),          
        ))                
      
      
      
      ucl_send_kind_list = ()
      is_o = ""
      if DEFAULT_OUTPUT_TYPE=="DEFAULT":
        is_o = my18.auto("●")
      else:
        is_o = my18.auto("　")
      ucl_send_kind_list = ucl_send_kind_list + (('%s%s%s %s' % (my18.auto("【"),is_o,my18.auto("】"),my18.auto("正常出字模式")) , None, [self.m_output_type,"DEFAULT"] ),)      
      
      
      if DEFAULT_OUTPUT_TYPE=="BIG5":
        is_o = my18.auto("●")
      else:
        is_o = my18.auto("　")
      ucl_send_kind_list = ucl_send_kind_list + (('%s%s%s %s' % (my18.auto("【"),is_o,my18.auto("】"),my18.auto("BIG5模式")) , None, [self.m_output_type,"BIG5"] ),)
      
      if DEFAULT_OUTPUT_TYPE=="PASTE":
        is_o = my18.auto("●")
      else:
        is_o = my18.auto("　")
      ucl_send_kind_list = ucl_send_kind_list + (('%s%s%s %s' % (my18.auto("【"),is_o,my18.auto("】"),my18.auto("複製貼上模式")) , None, [self.m_output_type,"PASTE"] ),)
      
        
      menu_options = menu_options + (((my18.auto("3.選擇出字模式"), None, ucl_send_kind_list),))       
            
      #2021-12-01 加入畫面操作相關
      _menu_ui_arr = ()
      debug_print("SHORT_MODE:");
      debug_print(config["DEFAULT"]["SHORT_MODE"]);
      if config["DEFAULT"]["SHORT_MODE"] == "1":
        _menu_ui_arr = _menu_ui_arr + ((my18.auto('【●】短版模式') , None, [self.m_run_long] ),)         
      else:
        _menu_ui_arr = _menu_ui_arr + ((my18.auto('【　】短版模式') , None, [self.m_run_short] ),)
      
      _menu_ui_arr = _menu_ui_arr + ((my18.auto('【,,,+】畫面加大') , None, [self.m_ui_plus] ),)
      _menu_ui_arr = _menu_ui_arr + ((my18.auto('【,,,-】畫面縮小') , None, [self.m_ui_minus] ),)
        
      #英數時透明度
      _menu_ui_en_alpha_arr = ()
      for i in range(0,11):
        is_o = my18.auto("　")
        if str(int(float(config['DEFAULT']['NON_UCL_ALPHA'])*10)) == str(i):
          is_o = my18.auto("●")
        _menu_ui_en_alpha_arr = _menu_ui_en_alpha_arr + (('%s%s%s %d %%' % ( my18.auto("【"),is_o,my18.auto("】") , (i*10)) , None, [self.m_change_en_alpha, "%.1f" % (i/10.0) ] ),)
      _menu_ui_arr = _menu_ui_arr + (((my18.auto("英數時透明度") , None, _menu_ui_en_alpha_arr ),))
      
      #肥模式透明度
      _menu_ui_ucl_alpha_arr = ()
      for i in range(0,11):
        is_o = my18.auto("　")
        if str(int(float(config['DEFAULT']['ALPHA'])*10)) == str(i):
          is_o = my18.auto("●")
        _menu_ui_ucl_alpha_arr = _menu_ui_ucl_alpha_arr + (('%s%s%s %d %%' % ( my18.auto("【"),is_o , my18.auto("】"),(i*10)) , None, [self.m_change_ucl_alpha, "%.1f" % (i/10.0) ] ),)
      _menu_ui_arr = _menu_ui_arr + (((my18.auto("肥模式透明度") , None, _menu_ui_ucl_alpha_arr ),))        
        
      menu_options = menu_options + (((my18.auto("4.畫面調整"), None, _menu_ui_arr),))
                  
            
      if config['DEFAULT']['CTRL_SP'] == "1":
        menu_options = menu_options + ((
          (my18.auto("5.【●】使用 CTRL+SPACE 切換輸入法"), None, [self.m_ctrlsp_switch] ),          
        ))          
      else:
        menu_options = menu_options + ((
          (my18.auto("5.【　】使用 CTRL+SPACE 切換輸入法"), None, [self.m_ctrlsp_switch] ),          
        ))  
            
      if config['DEFAULT']['SP'] == "1":        
        menu_options = menu_options + ((
          (my18.auto("6.【●】顯示短根"), None, [self.m_sp_switch] ),
          
        ))   
      else:              
        menu_options = menu_options + ((
          (my18.auto("6.【　】顯示短根"), None, [self.m_sp_switch] ),          
        ))
        
      if config['DEFAULT']['SHOW_PHONE_CODE'] == "1":        
        menu_options = menu_options + ((
          (my18.auto("7.【●】顯示提示注音"), None, [self.m_show_phone_code_switch] ),
          
        ))   
      else:              
        menu_options = menu_options + ((
          (my18.auto("7.【　】顯示提示注音"), None, [self.m_show_phone_code_switch] ),          
        )) 
                   
      '''  
      if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1":
        menu_options = menu_options + ((
          ("8.【●】打字音", None, [self.m_pm_switch] ),          
        ))           
      else:
        menu_options = menu_options + ((
          ("8.【　】打字音", None, [self.m_pm_switch] ),          
        ))      
      # 接下來作打字音
      '''
      _menu_play_sound_arr = ()
      is_o = ""
      if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1":
        is_o = my18.auto("●")
      else:
        is_o = my18.auto("　")
      _menu_play_sound_arr = _menu_play_sound_arr + (('%s%s%s %s' % (my18.auto("【"),is_o,my18.auto("】"),my18.auto("打字音啟動")) , None, [self.m_pm_switch] ),)
      
      #接下來是打字音量
      for i in range(1,11):
        is_o = my18.auto("　")
        if config['DEFAULT']['KEYBOARD_VOLUME'] == str(i*10):
          is_o = my18.auto("●")
        _menu_play_sound_arr = _menu_play_sound_arr + (('%s%s%s %s %%' % (my18.auto("【"),is_o,my18.auto("】"),str(i*10)) , None, [self.m_pm_volume_switch,i*10] ),)
      
          
      menu_options = menu_options + (((my18.auto("8.打字音"), None, _menu_play_sound_arr),))
      
      '''
      sound_level_list = ()
      for i in range(0,11):        
        v = i*10
        real_v = i*100        
        is_o = "　"
        if NOW_VOLUME == real_v:
          is_o = my18.auto("●")
        if i == 0:
          sound_level_list = sound_level_list + (('【%s】靜音' % (is_o) , None, [self.m_change_volume,real_v] ),)
        else:
          sound_level_list = sound_level_list + (("【%s】%s %%" % (is_o,v), None, [self.m_change_volume,real_v]),)
                                                     
      menu_options = menu_options + ((
                ('3.打字音大小', None, sound_level_list),))
      '''  
        
      if config['DEFAULT']['STARTUP_DEFAULT_UCL'] == "1":
        menu_options = menu_options + ((
          (my18.auto("9.【●】啟動預設為「肥」模式"), None, [self.m_sdu_switch] ),          
        ))          
      else:
        menu_options = menu_options + ((
          (my18.auto("9.【　】啟動預設為「肥」模式"), None, [self.m_sdu_switch] ),          
        ))        
        
      if config['DEFAULT']['ENABLE_HALF_FULL'] == "1":
        menu_options = menu_options + ((
          (my18.auto("10.【●】允許(Shift+Space)切換 全形/半形"), None, [self.m_halffull_switch] ),          
        ))
      else:
        menu_options = menu_options + ((
          (my18.auto("10.【　】允許(Shift+Space)切換 全形/半形"), None, [self.m_halffull_switch] ),          
        ))
        
      menu_options = menu_options + ((my18.auto("11. 離開(Quit)"), None, [self.m_quit]),)
      if self.systray=="":
        #ICON_PATH
        #UCL_PIC_BASE64
        #"data:image/png;base64,"
        self.systray = SysTrayIcon(ICON_PATH, "%s %s" % (my18.auto("肥米輸入法："),VERSION) , menu_options) #, on_quit=self.m_quit)        
        self.systray.start()
      else:        
        self.systray.update(menu_options=menu_options)
    def m_sdu_switch(self,event,data=None):
      #啟動時，預設為肥模式，或英模式
      global config      
      if config['DEFAULT']['STARTUP_DEFAULT_UCL'] == "0":
         config['DEFAULT']['STARTUP_DEFAULT_UCL'] = "1"
      else:
         config['DEFAULT']['STARTUP_DEFAULT_UCL'] = "0"
      #切換後，都要存設定
      saveConfig()    
      self.reload_tray()        
    def m_halffull_switch(self,event,data=None):
      #啟動時，預設為允許切換全半形
      global config      
      if config['DEFAULT']['ENABLE_HALF_FULL'] == "0":
         config['DEFAULT']['ENABLE_HALF_FULL'] = "1"
      else:
         config['DEFAULT']['ENABLE_HALF_FULL'] = "0"
      #切換後，都要存設定
      saveConfig()    
      self.reload_tray()        
    def m_output_type(self,event,kind="DEFAULT"):
      global DEFAULT_OUTPUT_TYPE
      #debug_print(kind)
      DEFAULT_OUTPUT_TYPE = kind[0]
      self.reload_tray() 
    def m_sp_switch(self,event,data=None):
      global config
      if config['DEFAULT']['SP'] == "0":        
        config['DEFAULT']['SP']="1"
      else:
        config['DEFAULT']['SP']="0"
      #切換後，都要存設定
      saveConfig()
      self.reload_tray()   
    def m_show_phone_code_switch(self,event,data=None):
      global config
      if config['DEFAULT']['SHOW_PHONE_CODE'] == "0":        
        config['DEFAULT']['SHOW_PHONE_CODE']="1"
      else:
        config['DEFAULT']['SHOW_PHONE_CODE']="0"
      #切換後，都要存設定
      saveConfig()
      self.reload_tray()       
    def m_about(self,event,data=None):  # if i ommit the data=none section python complains about too much arguments passed on greetme
      message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
      message.set_position(gtk.WIN_POS_CENTER_ALWAYS)
      message.set_keep_above(True)
      _msg_text = about_uclliu()       
      message.set_markup( _msg_text )
      #toAlphaOrNonAlpha()
      message.show()
      toAlphaOrNonAlpha()  
      response = message.run()
      #toAlphaOrNonAlpha()
      debug_print("Show Version")
      #debug_print(response)
      #debug_print(gtk.ResponseType.BUTTONS_OK)
      if response == -5 or response == -4:
        #message.hide()
        message.destroy()
        #toAlphaOrNonAlpha()  
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()
        #return False
    def m_ctrlsp_switch(self,event,data=None):
      global config
      if config['DEFAULT']['CTRL_SP'] == "0":        
        config['DEFAULT']['CTRL_SP']="1"
      else:
        config['DEFAULT']['CTRL_SP']="0"
      #切換後，都要存設定
      saveConfig()
      self.reload_tray()                           
    def m_game_switch(self,event,data=None):
      global gamemode_btn_click
      global gamemode_btn      
      gamemode_btn_click(gamemode_btn)   
      self.reload_tray()       
    def m_pm_switch(self,event,data=None):
      #調整打字音開關
      global config
      #is_play_music
      if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "0":
         config['DEFAULT']['PLAY_SOUND_ENABLE'] = "1"
         #選完打字音，啟動後，會噹一聲
         play_sound()
      else:
         config['DEFAULT']['PLAY_SOUND_ENABLE'] = "0"
      #切換後，都要存設定
      saveConfig()
      self.reload_tray()  
    def m_pm_volume_switch(self,event,data=None):
      #調整打字音日音量
      global config
      #is_play_music      
      config['DEFAULT']['KEYBOARD_VOLUME'] = "%s" % (data[0])
      #然後播一下新的聲音大小
      play_sound()      
      #切換後，都要存設定
      saveConfig()
      self.reload_tray()       
    def m_quit(self,event,data=None):
      #self.systray.shutdown()      
      #global x_btn_click
      x_btn_click(self) 
      #self.reload_tray()  
      #ctypes.windll.user32.PostQuitMessage(0)
      #sys.exit(1)
    def m_none(self,data=None):
      return False
    def m_run_long(self,event,data=None):
      run_long()
      self.reload_tray()       
    def m_run_short(self,event,data=None):
      run_short()
      self.reload_tray() 
    def m_ui_plus(self,event,data=None):
      #畫面加大
      run_big_small(0.1)
      self.reload_tray()
    def m_ui_minus(self,event,data=None):
      #畫面縮小      
      run_big_small(-0.1)
      self.reload_tray()
    def m_change_en_alpha(self,event,data=None):
      #調整英數時的透明度
      config['DEFAULT']['NON_UCL_ALPHA'] = "%.1f" % (float(data[0]))
      toAlphaOrNonAlpha()
      saveConfig()
      self.reload_tray()
    def m_change_ucl_alpha(self,event,data=None):
      #調整UCL時的透明度
      config['DEFAULT']['ALPHA'] = "%.1f" % (float(data[0]))
      toAlphaOrNonAlpha()
      saveConfig()
      self.reload_tray()
    #def m_change_volume(self,event,new_volume):
    #  global NOW_VOLUME      
    #  NOW_VOLUME = new_volume[0]      
    #  #然後播一下新的聲音大小
    #  play_sound()
    #  self.reload_tray()    

# generator tray
tray = TrayIcon()


win.Show()
simple_btn.Show(False)

if config["DEFAULT"]["SHORT_MODE"] == "1":
  run_short()
else:
  run_long()  
  


#win.SetFocus(None)

# 初使化按二次
#uclen_btn_click(uclen_btn)
#uclen_btn_click(uclen_btn)

#set_interval(1)
if config['DEFAULT']['STARTUP_DEFAULT_UCL'] == "0":
  # 2021-08-08 使用者希望啟動時，為 英 模式
  uclen_btn_click(uclen_btn)
#gtk.main()

FlagStopUpdateGUI = False
def updateGUI():
  #global updateGUI_Step
  global FlagStopUpdateGUI
  updateGUI_Step = 0
  while True:
    time.sleep(0.01)
    #global is_shutdown
    #while gtk.events_pending():
      #gtk.main_iteration(False)
    if FlagStopUpdateGUI == True:
      break
    updateGUI_Step = updateGUI_Step + 1
    if updateGUI_Step % 30 == 0:
      updateGUI_Step = 0
      toAlphaOrNonAlpha()
      #print("GGG") 
      #SendKeysCtypes.SendKeys("gggxxxx")
      
#while True:
  #time.sleep(0.01)
  #debug_print("gg")
  #updateGUI() 
my_thread_updateGUI = thread.Thread(target=updateGUI)
my_thread_updateGUI.start()
 

 
pythoncom.PumpMessages()     



#app.MainLoop()
 