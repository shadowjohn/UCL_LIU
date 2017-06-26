import Tkinter as tk
import ttk

class Example(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.floater = FloatingWindow(self)

class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.wm_geometry("400x400+100+100")

        self.label = tk.Label(self, text="Grab the lower-right corner to resize")
        self.label.pack(side="top", fill="both", expand=True)

        self.grip = ttk.Sizegrip(self)
        self.grip.place(relx=0.8, rely=0.8, anchor="se")
        self.grip.lift(self.label)
        self.grip.bind("<B1-Motion>", self.OnMotion)


    def OnMotion(self, event):
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        self.geometry("%sx%s" % ((x1-x0),(y1-y0)))
        return

app=Example()
app.mainloop()