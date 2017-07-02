# -*- coding: utf-8 -*-
#from Tkinter import *
import pythoncom, pyHook
from pyHook import HookManager
from pyHook.HookManager import HookConstants 
import portalocker
import os
import sys
#import ttk
import gtk
from gtk import gdk
import win32clipboard
import pango

#import threading
from functools import wraps
#http://fredericiana.com/2014/11/14/settimeout-python-delay/

#用來送key的 https://stackoverflow.com/questions/136734/key-presses-in-python
#import pyautogui

#http://wiki.alarmchang.com/index.php?title=Python_%E5%AD%98%E5%8F%96_Windows_%E7%9A%84%E5%89%AA%E8%B2%BC%E7%B0%BF_ClipBoard_%E7%AF%84%E4%BE%8B
import win32gui
import win32process
import psutil
import win32com
import win32con
import win32com.client
import win32clipboard

#from win32api import GetSystemMetrics
#screen_width=GetSystemMetrics(0)
#screen_height=GetSystemMetrics(1)

import ctypes
user32 = ctypes.windll.user32
screen_width=user32.GetSystemMetrics(0)
screen_height=user32.GetSystemMetrics(1)

#https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
#import xerox
#import pyperclip
import php
my = php.kit()
reload(sys)
sys.setdefaultencoding('utf-8')

flag_is_shift_down=False
flag_is_play_otherkey=False
play_ucl_label=""
ucl_find_data=[]

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

def pleave(self, event):
  my.exit();

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
  
uclcode = my.json_decode(my.file_get_contents("liu.json"))
#print(uclcode)
def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap
@delay(0.1)
def my_gtk_refresh():
  #global OnMotion
  global win
  #win.gtk_main_iteration();
  dir(win)      

def toggle_ucl():
  global uclen_btn
  global play_ucl_label
  if uclen_btn.get_label()=="肥":
    uclen_btn.set_label("英")
    play_ucl_label=""
    type_label_set_text()
  else:
    uclen_btn.set_label("肥")
  uclen_label=uclen_btn.get_child()
  uclen_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))    
def is_ucl():
  global uclen_btn  
  #print("WTF: %s" % uclen_btn.get_label())
  if uclen_btn.get_label()=="肥":
    return True
  else:
    return False
def x_btn_click(self):
  print("Bye Bye");
  sys.exit()
# draggable
def winclicked(self, event):
  self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  pass
def uclen_btn_click(self):
  #print(dir(self))
  kind=self.get_label()
  if kind=="肥":
    self.set_label("英")
  else:
    self.set_label("肥")
  uclen_label=self.get_child()
  uclen_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
  pass
def hf_btn_click(self):
  kind=self.get_label()
  if kind=="半":
    self.set_label("全")
  else:
    self.set_label("半")
  hf_label=self.get_child()
  hf_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
  pass
def is_hf(self):
  global hf_btn
  c = hf_btn.get_child()
  kind = c.get_label()
  return (kind=="半")  
def mybtn_click(self):
  print("DIe")    
# http://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
def type_label_set_text():
  global type_label
  global play_ucl_label
  type_label.set_label(play_ucl_label)
  type_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
  if my.strlen(play_ucl_label) > 0:
    print("ShowSearch")
    show_search()
    pass
  else:    
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
    pass 
  return True
def word_label_set_text():
  global word_label
  global ucl_find_data 
  global play_ucl_label
  if play_ucl_label == "":
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
    return
  step=0
  m = []
  try:  
    for k in ucl_find_data:
      m.append("%d%s" % (step,k))
      step=step+1
    tmp = my.implode(" ",m)
    word_label.set_label(tmp)
    word_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
    return True
  except:
    play_ucl_label=""
    play_ucl("")
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))  
    return True
def show_search():
  #真的要顯示了
  global play_ucl_label
  global ucl_find_data
  print("ShowSearch1")
  c = my.strtolower(play_ucl_label)
  c = my.trim(c)
  print("ShowSearch2")
  if c in uclcode["chardefs"]:
    ucl_find_data = uclcode["chardefs"][c]
    word_label_set_text()
    return True
  else:
    return False  
  
  #print(find)
  #print("ShowSearch3")
  #print("FIND: [%s] %s" % (play_ucl_label,find))
  #pass
def play_ucl(thekey):
  global type_label
  global play_ucl_label
  play_ucl_label = type_label.get_label();
  play_ucl_label = "%s%s" % (play_ucl_label,thekey)
  type_label_set_text()
  return True
def senddata(data):
  global play_ucl_label
  global ucl_find_data
  #win32clipboard.OpenClipboard()
  #orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
  #win32clipboard.CloseClipboard()
  
  win32clipboard.OpenClipboard() 
  win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常
  win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
  win32clipboard.CloseClipboard()
  
  # ctrl + v
  #win32clipboard.OpenClipboard() 
  #win32clipboard.GetClipboardData(win32con.CF_TEXT) 
  #win32clipboard.CloseClipboard()
   
  play_ucl_label=""
  type_label_set_text()
  ucl_find_data=[]
           
  shell = win32com.client.Dispatch("WScript.Shell")
  
  hwnd = win32gui.GetForegroundWindow()
  pid = win32process.GetWindowThreadProcessId(hwnd)
  pp="";
  if len(pid) >=2:
    pp=pid[1]
  else:
    pp=pid[0]
  #print("PP:%s" % (pp))
  p=psutil.Process(pp)
  #print("PPPP:%s" % (p.exe()))
  f_arr = [ "putty","pietty","pcman" ]
  check=True
  for k in f_arr:
    if my.is_string_like(my.strtolower(p.exe()),k):
      check=False
      shell.SendKeys("+{INSERT}", 0)  
  if check==True:
    shell.SendKeys("^v", 0)
  

  
  #win32clipboard.OpenClipboard()
  #win32clipboard.EmptyClipboard()
  #win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
  #win32clipboard.CloseClipboard()
def OnKeyboardEvent(event):
  global flag_is_shift_down
  global flag_is_play_otherkey
  global play_ucl_label
  global ucl_find_data
  #print(dir())  
  #try:  
  #print(event)
  #print 'MessageName:',event.MessageName
  #print 'Message:',event.Message
  #print 'Time:',event.Time
  #print 'Window:',event.Window
  #print 'WindowName:',event.WindowName
  print 'Ascii:', event.Ascii, chr(event.Ascii)
  print 'Key:', event.Key
  print 'KeyID:', event.KeyID
  #print 'ScanCode:', event.ScanCode
  #print 'Extended:', event.Extended
  #print 'Injected:', event.Injected
  #print 'Alt', event.Alt
  #print 'Transition', event.Transition
  #print 'IS_UCL', is_ucl()
  #print '---'
  
  #thekey = chr(event.Ascii)
  if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift"):
    flag_is_shift_down=True
    flag_is_play_otherkey=False
  if event.MessageName == "key down" and event.Key != "Lshift" and event.Key != "Rshift":
    flag_is_play_otherkey=True        
  if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
    flag_is_shift_down=False
  if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
    #shift
    flag_is_shift_down=False
    print("Press shift")
    if flag_is_play_otherkey==False:
      toggle_ucl()
      print("Debug15")
    print("Debug14")
    return True
  if event.MessageName == "key down" and event.Ascii==32 and flag_is_shift_down==True:
    # Press shift and space
    # switch 半/全
    hf_btn_click(hf_btn)
    flag_is_play_otherkey=True
    flag_is_shift_down=False
    print("Debug13")
    return False            
  if is_ucl():
    if event.MessageName == "key down" and ( event.Ascii>=48 and event.Ascii <=57): #0~9
      # play key
      print("chr(event.Ascii): %s" % chr(event.Ascii))
      if len(ucl_find_data)>=1 and int(chr(event.Ascii)) < len(ucl_find_data):
        # send data
        data = ucl_find_data[int(chr(event.Ascii))]
        senddata(data)
        print("Debug12")
        return False
      else:
        if len(event.Key) == 1 and is_hf(None)==False:
          k = widen(event.Key)
          print("event.Key to Full:%s %s" % (event.Key,k))
          senddata(k)
          print("Debug11")
          return False
        print("Debug10")
        return True
    if event.MessageName == "key down" and ( (event.Ascii>=65 and event.Ascii <=90) or (event.Ascii>=97 and event.Ascii <=122) or event.Ascii==44 or event.Ascii==46 or event.Ascii==39 or event.Ascii==91 or event.Ascii==93 ):
      flag_is_play_otherkey=True
      if flag_is_shift_down==True:
        if len(event.Key) == 1 and is_hf(None)==False:
          k = widen(event.Key)
          print("285 event.Key to Full:%s %s" % (event.Key,k))
          senddata(k)
          print("Debug9")
          return False
        print("Debug8")
        return True
      else:
        # Play ucl
        #print("Play UCL")
        #print(thekey)
        play_ucl(chr(event.Ascii))
        print("Debug7")
        return False    
    if event.MessageName == "key down" and ( event.Ascii == 8 ):
      # ←
      if my.strlen(play_ucl_label) <= 0:                    
        play_ucl_label=""
        play_ucl("")
        print("Debug6")
        return True
      else:
        play_ucl_label = play_ucl_label[:-1]
        type_label_set_text()
        print("Debug5")        
        return False          
    if event.MessageName == "key down" and event.Ascii==32 :
      # Space      
      if len(ucl_find_data)>=1:
        
        #丟出第一個字
        print("Ggggggg")
        #pyautogui.typewrite(my.utf8tobig5("幹"))
        #shell = win32com.client.Dispatch("WScript.Shell")
        #shell.SendKeys("{ASC " + ucl_find_data[0] + "}", 0)
        #xerox.copy(u'some string')
        #xerox.paste(xsel=True)
        #pyperclip.copy("here we go")
        #pyperclip.paste()
        # ctrl + c
        #將一段文字Copy 到剪貼簿裡面等於按下 Control + C
        text = ucl_find_data[0]
        #] my.utf8tobig5("好的")
        senddata(text)
        
        
        print("Debug4")
        return False 
      else:
        print("Debug1")
        return True   
    else:
      print("Debug2")    
      return True
  else:
    print("Debug3")
    #if event.MessageName == "key up" and len(event.Key) == 1 and is_hf(None)==False:
    #  k = widen(event.Key)
    #  print("335 event.Key to Full:%s %s" % (event.Key,k))
    #  senddata(k)
    #  return False
    #if len(event.Key) == 1 and is_hf(None)==False and event.KeyID !=0 and event.KeyID !=145 and event.KeyID !=162:
    #  k = widen(event.Key)      
    #  senddata(k)
    print(event.Transition)
    if event.MessageName == "key down" and len( str(chr(event.Ascii)) ) == 1 and is_hf(None)==False and event.Injected == 0:
      k = widen( str(chr(event.Ascii)) )
      #print("ｋｋｋｋｋｋｋｋｋｋｋｋｋｋｋK:%s" % k)
      senddata(k)
      return False
    return True
    
      
  #except:
    #play_ucl_label=""
    #play_ucl("")
  #  print sys.exc_info()
  #  return False       
    

        
      
#程式主流程
#功能說明
#此是防止重覆執行
if os.path.isdir("C:\\temp") == False:
  os.mkdir("c:\\temp")
check_file_run = open('c:\\temp\\pyLiu.txt', "a+")
try:  
  portalocker.lock(check_file_run, portalocker.LOCK_EX | portalocker.LOCK_NB)

except:
  sys.exit(0)                      
   
   



#my_gtk_refresh()
#win.connect("destroy",lambda wid:gtk.main_quit())


#r = Tk()
#r.overrideredirect(True)
#r.wm_geometry("400x400+100+100")
#r.overrideredirect(True)
#r.wm_geometry("400x400+100+100")
#root.geometry("450x50+%d+%d" % (screen_width-450-300, screen_height - 50 - 300)) #550x250+%d+%d" % (screen_width/2-275, screen_height/2-125))
#root.call('wm', 'attributes', '.', '-topmost', True)
#root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False) 
#root.title("app")
#listbox=Listbox(Toplevel(root.master,width=150).overrideredirect(True),width=150).pack
#new_top = Toplevel(root.master,width=150)
#new_top.overrideredirect(True)
#root.listbox = Listbox(new_top,width=150)
#root.listbox.pack()



#label = Label(root, text="Grab the lower-right corner to resize")
#label.pack(side="top", fill="both", expand=True)
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()
#grip = ttk.Sizegrip(root)
#grip.place(relx=1.0, rely=1.0, anchor="se")
#grip.lift(label)
#grip.bind("<B1-Motion>", OnMotion)


    



#root.lift () 

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyAll = OnKeyboardEvent
print(dir(hm))
# set the hook
hm.HookKeyboard()
# wait forever

#root = Tk()
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()
#root=None


win=gtk.Window()
win.set_decorated(False)
win.set_resizable(False)
win.move(screen_width-600,screen_height-150)
#always on top
win.set_keep_above(True)
win.set_skip_taskbar_hint(False)  
win.set_skip_pager_hint(False)
win.set_decorated(False)
win.add_events( gdk.BUTTON_PRESS_MASK)
win.connect ('button-press-event', winclicked)


vbox = gtk.VBox(False)

hbox=gtk.HBox()
vbox.pack_start(hbox, False)

#button=gtk.Button("TEST")
#button.connect("clicked",mybtn_click)
#win.add(button)
uclen_btn=gtk.Button("肥")
uclen_label=uclen_btn.get_child()
uclen_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
uclen_btn.connect("clicked",uclen_btn_click)
uclen_btn.set_size_request(40,40)
hbox.add(uclen_btn)



hf_btn=gtk.Button("半")
hf_label=hf_btn.get_child()
hf_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
hf_btn.connect("clicked",hf_btn_click)
hf_btn.set_size_request(40,40)
hbox.add(hf_btn)

type_label=gtk.Label("")
type_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
type_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
type_label.set_size_request(100,40)
type_label.set_alignment(xalign=0.1, yalign=0.5) 
f_type = gtk.Frame()
f_type.add(type_label)
hbox.add(f_type)

word_label=gtk.Label("")
word_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
word_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
word_label.set_size_request(350,40)
word_label.set_alignment(xalign=0.05, yalign=0.5)
f_word = gtk.Frame()
f_word.add(word_label)
hbox.add(f_word)


x_btn=gtk.Button("╳")
x_label=uclen_btn.get_child()
x_label.modify_font(pango.FontDescription('微軟正黑體 bold 22'))
x_btn.connect("clicked",x_btn_click)
x_btn.set_size_request(40,40)
hbox.add(x_btn)

win.add(vbox)
win.show_all()
win.set_focus(None)
gtk.main()

pythoncom.PumpMessages()  



mainloop()  


    