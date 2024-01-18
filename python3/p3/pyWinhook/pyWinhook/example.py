from __future__ import print_function
import pyWinhook as pyHook

def OnMouseEvent(event):
  print('MessageName: %s' % event.MessageName)
  print('Message: %s' % event.Message)
  print('Time: %s' % event.Time)
  print('Window: %s' % event.Window)
  print('WindowName: %s' % event.WindowName)
  print('Position: (%d, %d)' % event.Position)
  print('Wheel: %s' % event.Wheel)
  print('Injected: %s' % event.Injected)
  print('---')

  # return True to pass the event to other handlers
  # return False to stop the event from propagating
  return True

def OnKeyboardEvent(event):
  print('MessageName: %s' % event.MessageName)
  print('Message: %s' % event.Message)
  print('Time: %s' % event.Time)
  print('Window: %s' % event.Window)
  print('WindowName: %s' % event.WindowName)
  print('Ascii: %s' %  event.Ascii, chr(event.Ascii))
  print('Key: %s' %  event.Key)
  print('KeyID: %s' %  event.KeyID)
  print('ScanCode: %s' %  event.ScanCode)
  print('Extended: %s' %  event.Extended)
  print('Injected: %s' %  event.Injected)
  print('Alt %s' %  event.Alt)
  print('Transition %s' %  event.Transition)
  print('---')

  # return True to pass the event to other handlers
  # return False to stop the event from propagating
  return True

# create the hook mananger
hm = pyHook.HookManager()
# register two callbacks
hm.MouseAllButtonsDown = OnMouseEvent
hm.KeyDown = OnKeyboardEvent

# hook into the mouse and keyboard events
hm.HookMouse()
hm.HookKeyboard()

if __name__ == '__main__':
  import pythoncom
  pythoncom.PumpMessages()
