import os
import sys
import json
from time import time
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
SbyS_trans = False
tarLan = 'zh-CN'

combineKey={
   'shift':0,
   'control':0,
   'menu':0,
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
    'ctrl':'control',
}


with open('stop.bat','w') as f:
    f.write('taskkill /pid {} /f\n'.format(os.getpid()))
    f.write('del %0')

class MyThread(threading.Thread):
    def __init__(self,text):
        threading.Thread.__init__(self)
        self.text = text
        self.hide = True
        self.last = ''

    def on_closing(self):
        self.app.withdraw()
        self.hide = True

    def show(self):
        self.hide = False
        self.app.update()
        self.app.deiconify()
    
    def LineSplit(self):
        global SbyS_trans
        SbyS_trans = not SbyS_trans
        self.Line['text'] = 'Line' if SbyS_trans else 'Whole'
        self.translate(oldInput=True)
    
    def changeLanguage(self):
        global tarLan
        tarLan = 'en' if tarLan == 'zh-CN' else 'zh-CN'
        self.Lang['text'] = tarLan[-2:].upper()
        self.translate(oldInput=True)

    def appendText(self):
        self.translate(append=True)

    def translate(self,append=False,oldInput=False):
        global SbyS_trans,tarLan
        info = pyperclip.paste()
        if len(info)==0: return
        if oldInput or self.last != info:
            if append:
                info = self.last + ' ' + info
                pyperclip.copy(info)
            self.last = info
            info = info.replace('\n',' ').replace('\r',' ')
            if SbyS_trans:
                info = info.replace('. ','.\n\n')
            trans = ''
            trans = GT(info,tarLan=tarLan)
            self.textBoard['text'] = trans
        if self.hide:
            self.show()
        self.app.update()
        w=self.app.winfo_screenwidth() - 350
        h=(self.app.winfo_screenheight() - self.app.winfo_height())//3
        self.app.geometry("+{}+{}".format(w,h)) 

    def Tcopy(self):
        pyperclip.copy(self.textBoard['text'])

    def run(self):
        self.app = tk.Tk()
        self.app.wm_attributes('-topmost', 1)
        self.app.overrideredirect(1)        
        frame = tk.Frame()
        frame.pack()
        self.Lang = tk.Button(frame, text="CN", command=self.changeLanguage, bg = "Gray",width=18, height=1)
        self.Line = tk.Button(frame, text="Whole", command=self.LineSplit,   bg = "Gray",width=18, height=1)
        btn = tk.Button(frame, text="X", command=self.on_closing, bg = "Red", width=4,  height=1)
        self.Lang.pack(side=tk.LEFT)
        self.Line.pack(side=tk.LEFT)
        btn.pack(side=tk.LEFT)

        self.textBoard = tk.Label(self.app, text=self.text, bg='white', width = 43, wraplength = 240, justify = 'left')
        self.textBoard.pack()
        copy = tk.Button(self.app, text="Copy", command=self.Tcopy, bg = "DeepSkyBlue", width=43, height=1)
        copy.pack()
        if self.text is None:
            self.translate()
        self.app.mainloop()

def onKeyUp(event):
    global combineKey
    for key in combineKey.keys():
        if key in event.Key:
            combineKey[key] = 0
            return True
    return True

def onKeyDown(event):
    global combineKey
    for key in combineKey.keys():
        if key in event.Key:
            combineKey[key] = time()
            return True
    for i in range(len(name)):
        if keys[i][-1] == event.Key:
            for k in keys[i][:-1]:
                if (time()-combineKey[k])>3: 
                    break
            else:
                func[i]()
            return True
    return True
        
if __name__ == "__main__":
    base = sys.path[0]
    with open(os.path.join(base,'setting.json'),'r') as f:
        dic = json.load(f)
    name = ['translate','append']
    keys = [[checkList[x] if x in checkList else x for x in dic[n]] for n in name]
    windowThread = MyThread(None)
    func = [windowThread.translate,windowThread.appendText]
    windowThread.start()
    hm = PyHook3.HookManager()
    hm.KeyDown = onKeyDown
    hm.KeyUp = onKeyUp
    hm.HookKeyboard()
    pythoncom.PumpMessages()
