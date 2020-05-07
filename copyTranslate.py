import os
import sys
import json
import PyHook3
import win32api
import win32gui
import pyperclip
import pythoncom
import threading
import tkinter as tk
from googleTrans import translate as GT

ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0, ct)
win32gui.ShowWindow(hd, 0)

# Listen Keyboard
textBoard = None
windowThread = None
SbyS_trans = False
tarLan = 'zh-CN'

combineKey={
   'shift':False,
   'ctrl':False,
   'menu':False,
}

checkList={
    ',':'Oem_Comma',
    '.':'Oem_Period',
    ';':'Oem_1',
    '/':'Oem_2',
    '`':'Oem_3',
    '[':'Oem_4',
    '\\':'Oem_5',
    ']':'Oem_6',
    '\'':'Oem_7',
    '-':'Oem_Minus',
    '=':'Oem_Plus',
    'Enter':'Return',
    'Esc':'Escape',
    'alt':'menu',
    'CapsLock':'Capital',
    'PageUp':'Prior',
    'PageDown':'Next',
    ' ':'Space',
}


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

def translate():
    global textBoard,windowThread,SbyS_trans,tarLan
    info = pyperclip.paste()
    if len(info)==0: return
    trans = info.replace('\n',' ').replace('\r',' ')
    if SbyS_trans:
        trans = trans.replace('. ','.\n\n')
    trans = GT(trans,tarLan=tarLan)
    if windowThread.hide:
        windowThread.show()
    textBoard['text'] = trans

def LineSplit():
    global SbyS_trans
    SbyS_trans = not SbyS_trans
    translate()

def changeLanguage():
    global tarLan
    tarLan = 'en' if tarLan == 'zh-CN' else 'zh-CN'
    translate()

func = [translate,LineSplit,changeLanguage]

def onKeyUp(event):
   global combineKey
   for key in combineKey.keys():
      if key in event.Key:
         combineKey[key] = False
         return True
   return True

def onKeyDown(event):
   global combineKey
   for key in combineKey.keys():
      if key in event.Key:
         combineKey[key] = True
         return True
   for i in range(3):
      for k in keys[i][:-1]:
         if not combineKey[k]: 
            break
      else:
         if keys[i][-1] == event.Key:
            func[i]()
            # print(name[i])
            return True
   return True
        
if __name__ == "__main__":
    base = sys.path[0]
    with open(os.path.join(base,'setting.json'),'r') as f:
        dic = json.load(f)
    name = ['translate','CH<->EN','LineSplit']
    keys = [[checkList[x] if x in checkList else x for x in dic[n]] for n in name]

    windowThread = MyThread(None)
    windowThread.start()
    hm = PyHook3.HookManager()
    hm.KeyDown = onKeyDown
    hm.KeyUp = onKeyUp
    hm.HookKeyboard()
    pythoncom.PumpMessages()
