import pygtk
#pygtk.require('2.0')
import gtk

#Just another test
#http://stackoverflow.com/questions/6782142/pygobject-left-click-menu-on-a-status-icon
#With this code we connect the status icon using "button-press-event"
#With this code, the SAME popup menu appears BOTH in right and left mouse click on gtkstatusicon.

class TrayIcon(gtk.StatusIcon):
    def __init__(self):
        gtk.StatusIcon.__init__(self)
        self.set_from_icon_name('help-about')
        self.set_has_tooltip(True)
        self.set_visible(True)
        self.connect("button-press-event", self.on_click)

    def greetme(self,data=None):  # if i ommit the data=none section python complains about too much arguments passed on greetme

        print ('greetme data',data)
        msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Greetings")
        msg.run()
        msg.destroy()

    def on_click(self,data,event): #data1 and data2 received by the connect action line 23
        print ('self :', self)
        print('data :',data)
        print('event :',event)
        btn=event.button #Bby controlling this value (1-2-3 for left-middle-right) you can call other functions.
        print('event.button :',btn)
        time=gtk.get_current_event_time() # required by the popup. No time - no popup.
        print ('time:', time)

        menu = gtk.Menu()

        menu_item1 = gtk.MenuItem("First Entry")
        menu.append(menu_item1)
        menu_item1.connect("activate", self.greetme) #added by gv - it had nothing before

        menu_item2 = gtk.MenuItem("Quit")
        menu.append(menu_item2)
        menu_item2.connect("activate", gtk.main_quit)

        menu.show_all()
        menu.popup(None, None, None, btn, time) #button can be hardcoded (i.e 1) but time must be correct.

if __name__ == '__main__':
    tray = TrayIcon()
    gtk.main()