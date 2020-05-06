import os
import PyHook3
import win32api
import win32gui
import pyperclip
import pythoncom
import threading
import tkinter as tk
from googleTrans import translate

ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0, ct)
win32gui.ShowWindow(hd, 0)

# Listen Keyboard
textBoard = None
windowThread = None

with open('stop.bat','w') as f:
    f.write('taskkill /pid {} /f\n'.format(os.getpid()))
    f.write('del %0')

class MyThread(threading.Thread):
    def __init__(self,text):
        threading.Thread.__init__(self)
        self.text = text
        self.hide = True

    def on_closing(self):
        self.app.withdraw()
        self.hide = True

    def show(self):
        self.hide = False
        self.app.update()
        self.app.deiconify()

    def run(self):
        global textBoard
        self.app = tk.Tk()
        self.app.wm_attributes('-topmost', 1)
        self.app.overrideredirect(1)
        w=self.app.winfo_screenwidth() - 350
        h=self.app.winfo_screenheight()//3
        self.app.geometry("+{}+{}".format(w,h))
        btn = tk.Button(self.app, text="Hide", command=self.on_closing, width=40, height=1, bg = "Gray")
        btn.pack()
        textBoard = tk.Label(self.app, text=self.text, bg='white', width = 40, wraplength = 240, justify = 'left')
        textBoard.pack()
        if self.text is None:
            self.app.withdraw()
        self.app.mainloop()

def onKeyboardEvent(event):
    global textBoard,windowThread
    if event.Ascii == 17:
        info = pyperclip.paste()
        if len(info)==0: return True
        trans = info.replace('\n',' ').replace('\r',' ')#.replace('. ','.\n')
        trans = translate(trans,oriLan='en')
        if windowThread.hide:
            windowThread.show()
        textBoard['text'] = trans
    return True
        
if __name__ == "__main__":
    windowThread = MyThread(None)
    windowThread.start()
    hm = PyHook3.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
