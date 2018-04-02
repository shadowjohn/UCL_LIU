#!/usr/bin/python
# -*- coding: utf-8 -*-
VERSION=1.1
is_DEBUG_mode = True
is_shutdown = False
def debug_print(data):
  global is_DEBUG_mode
  if is_DEBUG_mode==True:
    print(data)
import threading
import portalocker
import os
import re
import sys
import gtk
from gtk import gdk
import hashlib
import php             
my = php.kit()
reload(sys)
sys.setdefaultencoding('UTF-8')
def md5_file(fileName):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        print "Reading file has problem" , fileName
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest()


PWD=my.pwd()   


#此是防止重覆執行
check_file_run = open('/tmp/UCLLIU.lock', "a+")
try:  
  portalocker.lock(check_file_run, portalocker.LOCK_EX | portalocker.LOCK_NB)
except:
  md = gtk.MessageDialog(None, 
          gtk.DIALOG_DESTROY_WITH_PARENT, 
          gtk.MESSAGE_QUESTION, 
          gtk.BUTTONS_OK, "【肥米輸入法】已執行...")          
  md.set_position(gtk.WIN_POS_CENTER)
  response = md.run()            
  if response == gtk.RESPONSE_OK or response == gtk.RESPONSE_DELETE_EVENT:
    md.destroy()
    sys.exit(0)     

import pyxhook
from pyxhook import HookManager
import pango
import time

#http://wiki.alarmchang.com/index.php?title=Python_%E5%AD%98%E5%8F%96_Windows_%E7%9A%84%E5%89%AA%E8%B2%BC%E7%B0%BF_ClipBoard_%E7%AF%84%E4%BE%8B
import psutil

import ctypes

#check if exists tab cin json
is_need_trans_tab = False
is_need_trans_cin = False
is_all_fault = False
#my.unlink("liu.json")
#my.unlink("liu.cin")
if my.is_file("liu.json") == False:
  if my.is_file("liu.cin") == False:
    if my.is_file("liu-uni.tab") == False:
      is_all_fault=True
    else:
      is_need_trans_tab=True
      is_need_trans_cin=True   
  else:
    is_need_trans_cin=True  

# 2018-04-02 加入 fcitx 輸入法支援
if is_all_fault==True and my.is_file(PWD + "/fcitx_boshiamy.txt")==True:
  #將 fcitx_boshiamy.txt 轉成 正常的 liu.cin、然後轉成 liu.json
  debug_print("Run fcitx ...")
  my.copy(PWD+"/fcitx_boshiamy.txt",PWD+"/liu.cin");
  data = my.file_get_contents(PWD+"/liu.cin");
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
  #print(res) 
  for k in res:
    d=" ".join(k);
    data = data + d +"\n";  
  data = data + "%chardef end";
  my.file_put_contents(PWD+"/liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;  
  

if is_all_fault == True:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("無字根檔，請購買正版嘸蝦米，將「C:\\windows\\SysWOW64\\liu-uni.tab」或「C:\\Program Files\\BoshiamyTIP\\liu-uni.tab」與uclliu放在一起執行")  
  response = message.run()
  #print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    my.exit()
  #message.show()
  gtk.main()
           
if is_need_trans_tab==True:
  #需要轉tab檔                                                                             
  #Check liu-uni.tab md5 is fuck up
  if md5_file( ("%s/liu-uni.tab" % (PWD)) )== "4e89501681ba0405b4c0e03fae740d8c":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("請不要使用義守大學的字根檔，這組 liu-uni.tab 太舊不支援...");
    response = message.run()
    #print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      my.exit()
    #message.show()
    gtk.main()
  if md5_file( ("%s/liu-uni.tab" % (PWD)) )== "260312958775300438497e366b277cb4":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("此組字根檔並非正常的 liu-uni.tab，這個不支援...");
    response = message.run()
    #print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      my.exit()
    #message.show()
    gtk.main()
  import liu_unitab2cin
  #print(PWD)  
  liu_unitab2cin.convert_liu_unitab( ("%s/liu-uni.tab" % (PWD)), ("%s/liu.cin" % (PWD) ))

if is_need_trans_cin==True:
  import cintojson
  cinapp = cintojson.CinToJson()
  cinapp.run( "liu" , "liu.cin",False)


last_key = "" #to save last 7 word for game mode 
flag_is_win_down=False
flag_is_shift_down=False
flag_is_ctrl_down=False
flag_is_play_otherkey=False
play_ucl_label=""
ucl_find_data=[]
same_sound_data=[] #同音字表
same_sound_index=0 #預設第零頁
same_sound_max_word=6 #一頁最多五字
is_has_more_page=False #是否還有下頁
same_sound_last_word="" #lastword
# 用來出半型字的
# https://stackoverflow.com/questions/2422177/python-how-can-i-replace-full-width-characters-with-half-width-characters
HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000

WIDE_MAP = dict((i, i + 0xFEE0) for i in xrange(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
                  
def widen(s):
  #https://gist.github.com/jcayzac/1485005
  """
  Convert all ASCII characters to the full-width counterpart.
  
  >>> print widen('test, Foo!')
  ｔｅｓｔ，　Ｆｏｏ！
  >>> 
  """
  return unicode(s).translate(WIDE_MAP)

#def pleave(self, event):
#  my.exit();

if my.is_file("liu.json") == False:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("缺少liu.json")  
  response = message.run()
  #print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    my.exit()
  #message.show()
  gtk.main()
  #my.exit()
if my.is_file("pinyi.txt")==True:
  same_sound_data = my.explode("\n",my.trim(my.file_get_contents("pinyi.txt")))  
  
uclcode = my.json_decode(my.file_get_contents("liu.json"))
      
def toAlphaOrNonAlpha():
  global uclen_btn
  global hf_btn
  global win  
  #c = hf_btn.get_child()
  #hf_kind = c.get_label()
  hf_kind = hf_btn.get_label()
  if uclen_btn.get_label()=="英" and hf_kind=="半":
    win.set_opacity(0.2)
  else:
    win.set_opacity(1)
def toggle_ucl():
  global uclen_btn
  global play_ucl_label
  global win
  global debug_print
  if uclen_btn.get_label()=="肥":
    uclen_btn.set_label("英")
    play_ucl_label=""
    type_label_set_text()
    win.set_keep_above(False)
  else:
    uclen_btn.set_label("肥")
    win.set_keep_above(True)
  uclen_label=uclen_btn.get_child()
  uclen_label.modify_font(pango.FontDescription('標楷體 bold 22'))
                                              
  #window_state_event_cb(None,None)
  debug_print("window_state_event_cb(toggle_ucl)")
  toAlphaOrNonAlpha()    
def is_ucl():
  global uclen_btn  
  #print("WTF: %s" % uclen_btn.get_label())
  if uclen_btn.get_label()=="肥":
    return True
  else:
    return False
def gamemode_btn_click(self):
  global gamemode_btn 
  if gamemode_btn.get_label()=="正常模式":
    gamemode_btn.set_label("遊戲模式")
    if uclen_btn.get_label() == "肥":
      uclen_btn_click(uclen_btn)    
  else:
    gamemode_btn.set_label("正常模式")
def x_btn_click(self):
  print("Bye Bye");
  global is_shutdown
  is_shutdown = True
  #sys.exit(1)
# draggable
def winclicked(self, event):
  # make UCLLIU can draggable
  self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  pass
def uclen_btn_click(self):
  toggle_ucl()
  #pass
def hf_btn_click(self):
  kind=self.get_label()
  if kind=="半":
    self.set_label("全")
  else:
    self.set_label("半")
  hf_label=self.get_child()
  hf_label.modify_font(pango.FontDescription('標楷體 bold 22'))
  toAlphaOrNonAlpha()
  pass
def is_hf(self):
  global hf_btn
  c = hf_btn.get_child()
  kind = c.get_label()
  return (kind=="半")
   
# http://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
def type_label_set_text():
  global type_label
  global play_ucl_label
  global debug_print
  type_label.set_label(play_ucl_label)
  type_label.modify_font(pango.FontDescription('標楷體 bold 22'))
  if my.strlen(play_ucl_label) > 0:
    debug_print("ShowSearch")
    show_search()
    pass
  else:    
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription('標楷體 bold 20'))
    pass 
  return True
def word_label_set_text():
  global word_label
  global ucl_find_data 
  global play_ucl_label
  global is_has_more_page
  if play_ucl_label == "":
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription('標楷體 bold 20'))
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
    word_label.set_label(tmp)
    word_label.modify_font(pango.FontDescription('標楷體 bold 20'))
    return True
  except:
    play_ucl_label=""
    play_ucl("")
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription('標楷體 bold 20'))  
    return True
def show_search():
  #真的要顯示了
  global play_ucl_label
  global ucl_find_data
  global is_need_use_pinyi
  global is_has_more_page
  global same_sound_index
  global same_sound_last_word
  global debug_print
  same_sound_index = 0
  is_has_more_page=False
  same_sound_last_word=""
  debug_print("ShowSearch1")
  c = my.strtolower(play_ucl_label)
  c = my.trim(c)
  #print("ShowSearch2")
  #print("C[-1]:%s" % c[-1])
  #print("C[:-1]:%s" % c[:-1])  
  # 此部分可以修正 V 可以出第二字，還不錯
  # 2017-07-13 Fix when V is last code
  #print("LAST V : %s" % (c[-1]))
  is_need_use_pinyi=False  
  if c[0] == "'" and len(c)>1:
    c=c[1:]
    is_need_use_pinyi=True
  if c not in uclcode["chardefs"] and c[-1]=='v' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=2 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][1]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='r' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=3 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][2]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='s' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=4 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][3]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='f' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=5 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][4]   
    word_label_set_text()
    return True
  elif c in uclcode["chardefs"]:
    #print("Debug V2")
    ucl_find_data = uclcode["chardefs"][c]
    word_label_set_text()
    return True
  else:
    #print("Debug V3")
    ucl_find_data=[]  
    #play_ucl_label=""  
    ucl_find_data=[]
    word_label_set_text()
    return False  
  
  #print(find)
  #print("ShowSearch3")
  #print("FIND: [%s] %s" % (play_ucl_label,find))
  #pass
def play_ucl(thekey):
  global type_label
  global play_ucl_label
  play_ucl_label = type_label.get_label();
  # 不可以超過5個字
  if len(play_ucl_label) < 5:
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
  
  same_sound_index=0 #回到第零頁
  is_has_more_page=False #回到沒有分頁
  same_sound_last_word=""
  play_ucl_label=""
  ucl_find_data=[]  
  type_label_set_text()  
  
  #SendKeysCtypes.SendKeys(data.decode("UTF-8"),0)
  return
  shell = win32com.client.Dispatch("WScript.Shell")
  
  hwnd = win32gui.GetForegroundWindow()
  pid = win32process.GetWindowThreadProcessId(hwnd)
  pp="";
  if len(pid) >=2:
    pp=pid[1]
  else:
    pp=pid[0]
  #print("PP:%s" % (pp))
  debug_print("PP:%s" % (pp))
  p=psutil.Process(pp)
  f_arr = [ "putty","pietty","pcman","xyplorer" ]
  f_big5_arr = [ "zip32w" ]
  check_kind="0"
  for k in f_arr:
    #break;
    if my.is_string_like(my.strtolower(p.exe()),k):
      check_kind="1"      
      
      win32clipboard.OpenClipboard()
      orin_clip=""
      try:
        orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
      except:
        pass
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
      win32clipboard.EmptyClipboard()
      win32clipboard.CloseClipboard()
            
      win32clipboard.OpenClipboard() 
      win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
      win32clipboard.CloseClipboard()
      shell.SendKeys("+{INSERT}", 0) 
      #reload(sys)                                    
      #sys.setdefaultencoding('UNICODE') 
      #SendKeysCtypes.SendKeys("肥".encode("UTF-8",0))
      #reload(sys)                                    
      #sys.setdefaultencoding('UTF-8')
      #也許要設delay...
      time.sleep(0.05)
      win32clipboard.OpenClipboard()    
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      win32clipboard.CloseClipboard()            
      break
  for k in f_big5_arr:
    if my.is_string_like(my.strtolower(p.exe()),k):
      debug_print("Debug_f_big5_arr")
      #SendKeysCtypes.SendKeys(my.utf8tobig5(data))
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
      shell.SendKeys("^v", 0)
      time.sleep(0.05)
      win32clipboard.OpenClipboard()    
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      win32clipboard.CloseClipboard()         
      break
            
  if check_kind=="0":
    #reload(sys)                                    
    #sys.setdefaultencoding('UTF-8')
    #print("CP950")
    SendKeysCtypes.SendKeys(data.decode("UTF-8"),0)
    #reload(sys)
    #sys.setdefaultencoding('UTF-8')
  
  #reload(sys)                                    
  #sys.setdefaultencoding('auto')
  #SendKeysCtypes.SendKeys(data.decode("auto"),0)
  
def use_pinyi(data):
  global same_sound_data
  global ucl_find_data
  global same_sound_index
  global same_sound_max_word
  global is_has_more_page
  global debug_print
  finds=""
  for k in same_sound_data:
    if my.is_string_like(k,data):
      #if k.startswith(u'\xe7\x9a\x84'):
      #  k = u[1:]
      finds="%s%s " % (finds,my.trim(k))
      #print(k)
  finds=my.trim(finds);
  finds=my.explode(" ",finds)
  #print(finds)
  #finds=finds[:] 
  #for k in finds:
  #  print(k.encode("UTF-8"))
  finds = my.array_unique(finds)
  #print("Debug data: %s " % data.encode("UTF-8"))
  debug_print("Debug Finds: %d " % len(finds))
  debug_print("Debug same_sound_index: %d " % same_sound_index)
  debug_print("Debug same_sound_max_word: %d " % same_sound_max_word)  
  maxword = same_sound_index+same_sound_max_word
  if maxword >= len(finds)-1:
    maxword = len(finds)-1
    is_has_more_page = False
  else:
    is_has_more_page = True
  ucl_find_data=finds[same_sound_index:maxword]
  debug_print("DEBUG same_sound_index: %d " % same_sound_index)
  same_sound_index=same_sound_index+same_sound_max_word
   
  if same_sound_index>=len(finds):
    same_sound_index=0
  word_label_set_text()
  #finds=my.str_replace(data," ",finds)
  #finds=my.str_replace("  "," ",finds)
  
def OnKeyboardEvent(event):
  global last_key
  global flag_is_win_down
  global flag_is_shift_down
  global flag_is_ctrl_down
  global flag_is_play_otherkey
  global play_ucl_label
  global ucl_find_data
  global is_need_use_pinyi
  global same_sound_last_word
  global gamemode_btn
  global debug_print
  global VERSION
  #print(dir())  
  #try:  
  print(event.Key)
  print(event)
  print 'MessageName:',event.MessageName
  print 'Window:',event.Window
  print 'WindowName:',event.WindowName
  print 'Ascii:', event.Ascii, chr(event.Ascii)
  print 'Key:', event.Key
  print 'KeyID:', event.KeyID
  print 'ScanCode:', event.ScanCode
  print 'IS_UCL', is_ucl()
  print '---'
  #print 'last_key:', last_key[-8:]
  global hm
  print dir(hm)
  return False
  if event.MessageName == "key down":
    last_key = last_key + chr(event.Ascii)
    last_key = last_key[-10:]
    if my.strtolower(last_key[-7:])==",,,lock":
      last_key = ""
      if gamemode_btn.get_label()=="正常模式":
        gamemode_btn_click(gamemode_btn)
    if my.strtolower(last_key[-9:])==",,,unlock":          
      last_key = ""               
      if gamemode_btn.get_label()=="遊戲模式":
        gamemode_btn_click(gamemode_btn)
    if my.strtolower(last_key[-10:])==",,,version":
      last_key= ""   
      message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)      
      message.set_markup( ("肥米輸入法版本：%s" % VERSION) )
      message.show()  
      response = message.run()
      debug_print("Show Version")
      #print(gtk.ResponseType.BUTTONS_OK)
      if response == -5 or response == -4:
        #message.hide()  
        message.destroy()            
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        return False      
  #print("LAST_KEY:" + last_key)
  if gamemode_btn.get_label()=="遊戲模式":      
    return True    
  
  #thekey = chr(event.Ascii)
  # KeyID = 91 = Lwinkey
  if event.MessageName == "key down" and (event.KeyID == 91 or event.KeyID == 92):
    flag_is_win_down = True
    debug_print("Debug event A")
  if event.MessageName == "key up" and (event.KeyID == 91 or event.KeyID == 92):
    flag_is_win_down = False
    debug_print("Debug event B") 
  if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Shift_L" or event.Key == "Rshift" or event.Key == "Shift_R"):
    flag_is_shift_down=True
    debug_print("Debug event C")    
    flag_is_play_otherkey=False
  if event.MessageName == "key down" and (event.Key != "Lshift" and event.Key != "Rshift" and event.Key != "Shift_L" and event.Key != "Shift_R"):
    debug_print("Debug event D")
    flag_is_play_otherkey=True          
  if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Shift_L" or event.Key == "Rshift" or event.Key == "Shift_R"):
    debug_print("Debug event E")
    #shift
    flag_is_shift_down=False
    debug_print("Press shift")
    # 不可是右邊的2、4、6、8 
    if flag_is_play_otherkey==False and (event.Ascii > 40 or event.Ascii < 37) :
      toggle_ucl()
      debug_print("Debug15")    
    debug_print("Debug14")
    #toAlphaOrNonAlpha()
    return True
  if event.MessageName == "key down" and event.Ascii==32 and flag_is_shift_down==True:
    # Press shift and space
    # switch 半/全
    hf_btn_click(hf_btn)
    flag_is_play_otherkey=True
    flag_is_shift_down=False    
    debug_print("Debug13")
    return False            
  if is_ucl():    
    if event.MessageName == "key down" and flag_is_win_down == True : # win key
      return True 
    if event.MessageName == "key down" and ( event.Ascii>=48 and event.Ascii <=57) : #0~9 
      if len(ucl_find_data)>=1 and int(chr(event.Ascii)) < len(ucl_find_data):
        # send data        
        data = ucl_find_data[int(chr(event.Ascii))]
        senddata(data)
        debug_print("Debug12")
        return False
      else:
        if len(event.Key) == 1 and is_hf(None)==False:
          #k = widen(event.Key)
          kac = event.Ascii          
          k = widen(chr(kac))
          debug_print("event.Key to Full:%s %s" % (event.Key,k))
          senddata(k)
          debug_print("Debug11")
          return False
        
        debug_print("Debug10")
        #2017-10-24要考慮右邊數字鍵的狀況
        if is_hf(None)==False and ( event.Ascii==49 or event.Ascii==50 or event.Ascii==51 or event.Ascii==52 or event.Ascii==53 or event.Ascii==54 or event.Ascii==55 or event.Ascii==56 or event.Ascii==57 or event.Ascii==47 or event.Ascii==42 or event.Ascii==45 or event.Ascii==43 or event.Ascii==48 or event.Ascii==46):
          kac = event.Ascii        
          k = widen(chr(kac))
          senddata(k)
          debug_print("Debug100")
          return False
        else:  
          return True                    
    if event.MessageName == "key down" and ( (event.Ascii>=65 and event.Ascii <=90) or (event.Ascii>=97 and event.Ascii <=122) or event.Ascii==44 or event.Ascii==46 or event.Ascii==39 or event.Ascii==91 or event.Ascii==93 ):
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
          debug_print("285 event.Key to Full:%s %s" % (event.Key,k))
          senddata(k)
          debug_print("Debug9")
          return False
        debug_print("Debug8")
        return True
      else:
        # Play ucl
        #print("Play UCL")
        #print(thekey)
        play_ucl(chr(event.Ascii))
        debug_print("Debug7")
        return False    
    if event.MessageName == "key down" and ( event.Ascii == 8 ): # ←      
      if my.strlen(play_ucl_label) <= 0:                    
        play_ucl_label=""
        play_ucl("")
        debug_print("Debug6")
        return True
      else:
        play_ucl_label = play_ucl_label[:-1]
        type_label_set_text()
        debug_print("Debug5")        
        return False       
    if event.MessageName == "key down" and event.Ascii==32 : #空白
      # Space                          
      if len(ucl_find_data)>=1:        
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
          senddata(text)
        debug_print("Debug4")
        return False 
      elif len(ucl_find_data)==0 and len(play_ucl_label)!=0:
        #無此字根時，按到空白鍵
        debug_print("Debug11")
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
      #修正 肥/全 時，按分號、冒號只出半型的問題
      if is_hf(None)==False:        
        kac = event.Ascii        
        k = widen(chr(kac))
        senddata(k)
        debug_print("Debug22")
        return False
      else:
        debug_print("Debug22OK")
        return True     
    else:                  
      return True            
      
  else:
    debug_print("DDDDDDDDD: " + event.Key + "," + str(event.KeyID) + "," +  event.MessageName)
    debug_print("Debug3")  
    debug_print(event.KeyID)
    # 2018-03-27 此部分修正「英/全」時，按Ctrl A 無效的問題，或ctrl+esc等問題
    # 修正enter、winkey 在「英/全」的狀況
    if event.MessageName == "key down" and event.KeyID == 13:
      return True
    if event.MessageName == "key down" and ( event.KeyID == 91 or event.KeyID == 92): #winkey
      flag_is_win_down=True
      return True
    if event.MessageName == "key down" and flag_is_win_down == True : # win key
      flag_is_win_down=False
      return True    
    if event.MessageName == "key down" and ( event.KeyID == 231 or event.KeyID == 162 or event.KeyID == 163):
      flag_is_ctrl_down=True
      debug_print("Ctrl key")
      return True
    if flag_is_ctrl_down == True:
      flag_is_ctrl_down=False
      return True       
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
      if flag_is_play_otherkey==False:
        toggle_ucl()
        debug_print("Debug315")    
      debug_print("Debug314")
      return True
    
    #if event.MessageName == "key up" and len(event.Key) == 1 and is_hf(None)==False:
    #  k = widen(event.Key)
    #  print("335 event.Key to Full:%s %s" % (event.Key,k))
    #  senddata(k)
    #  return False
    #if len(event.Key) == 1 and is_hf(None)==False and event.KeyID !=0 and event.KeyID !=145 and event.KeyID !=162:
    #  k = widen(event.Key)      
    #  senddata(k) 
    #debug_print("Debug3: %s" % (event.Transition))
    if event.KeyID==8 or event.KeyID==20 or event.KeyID==45 or event.KeyID==46 or event.KeyID==36 or event.KeyID==33 or event.KeyID==34 or event.KeyID==35 or event.KeyID==160 or event.KeyID==161 or event.KeyID==9 or event.KeyID == 37 or event.KeyID == 38 or event.KeyID == 39 or event.KeyID == 40: #↑←→↓
      return True
    if event.MessageName == "key down" and len( str(chr(event.Ascii)) ) == 1 and is_hf(None)==False and event.Injected == 0 :
      k = widen( str(chr(event.Ascii)) )
      #print("ｋｋｋｋｋｋｋｋｋｋｋｋｋｋｋK:%s" % k)
      senddata(k)
      return False
    return True    
      
#程式主流程
#功能說明


# create a hook manager
hm = pyxhook.HookManager()
#hm.UnhookMouse();
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
hm.KeyUp = OnKeyboardEvent
print(dir(hm))
# set the hook
hm.HookKeyboard()
#hm.start()
# wait forever
hm_ready=threading.Event()
def run_hm_thread():
    #global hm
    #hm.start()
    pass
hm_thread = threading.Thread(target=run_hm_thread)
hm_thread.start()
#hm_ready.wait()
        
#win=gtk.Window(type=gtk.WINDOW_POPUP)
win=gtk.Window(type=gtk.WINDOW_POPUP)
win.set_modal(True)
win.set_resizable(False)

#取螢幕大小
#user32 = ctypes.windll.user32
screen_width=gtk.gdk.screen_width() 
#user32.GetSystemMetrics(0)
screen_height=gtk.gdk.screen_height()
#user32.GetSystemMetrics(1)

win.move(screen_width-700,screen_height-150)
#always on top
win.set_keep_above(True)
win.set_keep_below(False)
win.set_skip_taskbar_hint(False)  
win.set_skip_pager_hint(False)
win.set_decorated(False)
win.set_accept_focus(False)
win.set_icon_name(None)

win.add_events( gdk.BUTTON_PRESS_MASK)
win.connect ('button-press-event', winclicked)


vbox = gtk.VBox(False)

hbox=gtk.HBox()
vbox.pack_start(hbox, False)

uclen_btn=gtk.Button("肥")
uclen_label=uclen_btn.get_child()
uclen_label.modify_font(pango.FontDescription('標楷體 bold 22'))
uclen_btn.connect("clicked",uclen_btn_click)
uclen_btn.set_size_request(40,40)
hbox.add(uclen_btn)

hf_btn=gtk.Button("半")
hf_label=hf_btn.get_child()
hf_label.modify_font(pango.FontDescription('標楷體 bold 22'))
hf_btn.connect("clicked",hf_btn_click)
hf_btn.set_size_request(40,40)
hbox.add(hf_btn)

type_label=gtk.Label("")
type_label.modify_font(pango.FontDescription('標楷體 bold 22'))
type_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
type_label.set_size_request(100,40)
type_label.set_alignment(xalign=0.1, yalign=0.5) 
f_type = gtk.Frame()
f_type.add(type_label)
hbox.add(f_type)

word_label=gtk.Label("")
word_label.modify_font(pango.FontDescription('標楷體 bold 20'))
word_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
word_label.set_size_request(350,40)
word_label.set_alignment(xalign=0.05, yalign=0.5)
f_word = gtk.Frame()
f_word.add(word_label)
hbox.add(f_word)

gamemode_btn=gtk.Button("正常模式")
gamemode_label=uclen_btn.get_child()
gamemode_label.modify_font(pango.FontDescription('標楷體 bold 26'))
gamemode_btn.connect("clicked",gamemode_btn_click)
gamemode_btn.set_size_request(80,40)
hbox.add(gamemode_btn)

x_btn=gtk.Button("╳")
x_label=uclen_btn.get_child()
x_label.modify_font(pango.FontDescription('標楷體 bold 22'))
x_btn.connect("clicked",x_btn_click)
x_btn.set_size_request(40,40)
hbox.add(x_btn)




win.add(vbox)

win.show_all()
win.set_focus(None)
hm.start()
def updateGUI():
    global is_shutdown
    while gtk.events_pending():
        gtk.main_iteration(False)
#worker=threading.Thread(target=countdown,args(5,))
#worker.start()
while True:
    time.sleep(0.001)
    updateGUI()
#pythoncom.PumpMessages()     


#mainloop()  
 
