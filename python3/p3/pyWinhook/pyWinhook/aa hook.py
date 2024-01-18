from __future__ import print_function
import wx
import pyWinhook as pyHook
from pyAA import *
  
class myFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, 'My Frame')
    
    self.hm = pyHook.HookManager()
    self.hm.MouseAllButtonsDown = self.OnMouseEvent
    self.hm.KeyDown = self.OnKeyboardEvent
  
    self.hm.HookMouse()
    self.hm.HookKeyboard()
    
    wx.EVT_CLOSE(self, self.OnClose)
  
  def OnGetAO(self, event):
    if event.Type == 'keyboard':
      ao = AccessibleObjectFromWindow(event.Window, OBJID_CLIENT)
    elif event.Type == 'mouse':
      ao = AccessibleObjectFromPoint(event.Position)

    print('')
    print('---------------------------')
    print('Event:')
    print(' %s' % event.MessageName)
    print('  Window: %s' % event.WindowName)
    if event.Type == 'keyboard':
      print('  Key: %s' % event.Key)
    print('')
    print('Object:')
    try:
      print('  Name: %s' % ao.Name)
    except:
      print()
    
    try:
      print('  Value: %s' % ao.Value)
    except:
      print()

    try:
      print('  Role: %s' % ao.RoleText)
    except:
      print()
    
    try:
      print('  Description: %s' %ao.Description)
    except:
      print()
    
    try:
      print('  State: %s' % ao.StateText)
    except:
      print()
      
    try:
      print('  Shortcut: %s' % ao.KeyboardShortcut)
    except:
      print()
    
  def OnMouseEvent(self, event):
    event.Type = 'mouse'
    wx.CallAfter(self.OnGetAO, event)

  def OnKeyboardEvent(self, event):
    event.Type = 'keyboard'
    wx.CallAfter(self.OnGetAO, event)
    
  def OnClose(self, event):
    del self.hm
    self.Destroy()
  
if __name__ == '__main__':
  app = wx.PySimpleApp(0)
  frame = myFrame()
  app.SetTopWindow(frame)
  frame.Show()  
  app.MainLoop()
