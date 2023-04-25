import os
import sys
import json5 as json
from time import time
import PyHook3
import win32api
import win32gui
import pyperclip
import pythoncom
import threading
import tkinter as tk
import re
from googleTrans import translate as GT

os.environ['NO_PROXY'] = 'translate.google.com'
if len(sys.argv)==1:
    ct = win32api.GetConsoleTitle()
    hd = win32gui.FindWindow(0, ct)
    win32gui.ShowWindow(hd, 0)

# Listen Keyboard
SbyS_trans = False
tarLan = 'zh-CN'
trans_call = None
Trans_End = True

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

if len(sys.argv)==1:
    with open('stop.bat','w') as f:
        f.write('taskkill /pid {} /f\n'.format(os.getpid()))
        f.write('del %0')

#goods_rejection_info

class TransThread(threading.Thread):
    def __init__(self,text):
        threading.Thread.__init__(self)
        self.text = text

    def run(self):
        global tarLan,Trans_End
        trans = GT(self.text,tarLan=tarLan)
        if tarLan == 'zh-CN':
            underline_words = re.findall('\w*_\w*',trans)
            if len(underline_words)>0:
                trans_element = GT('\n\n'.join(underline_words).replace('_',' '),tarLan=tarLan).split('\n\n')
                trans_element = {j:f'{i}({j})'for i,j in zip(trans_element,underline_words)}
                trans = re.sub('\w*_\w*',lambda x: trans_element[x.group()],trans)
        windowThread.showTrans(trans)
        Trans_End = True

class UIThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.hide = True
        self.last = ''

    def on_closing(self):
        self.app.withdraw()
        self.hide = True

    def show(self):
        if not self.hide: return
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

    def showTrans(self,trans):
        if len(trans)==0: self.last = ''
        self.textBoard['text'] = trans
        self.show()
        self.copy['text'] = 'Copy'
        self.app.update()
        w=self.app.winfo_screenwidth() - 350
        h=(self.app.winfo_screenheight() - self.app.winfo_height())//3
        self.app.geometry("+{}+{}".format(w,h)) 

    def translate(self,append=False,oldInput=False):
        global SbyS_trans,Trans_End,trans_call,tarLan
        if not Trans_End: return
        if trans_call is not None: trans_call.join()
        info = pyperclip.paste()
        if len(info)==0: return
        if oldInput or self.last != info:
            if append:
                info = self.last + ' ' + info
                pyperclip.copy(info)
            self.last = info
            if tarLan == 'zh-CN':
                info = info.replace('\n',' ').replace('\r',' ')
            else:
                info = info.replace('\n','').replace('\r','')

            running_re_sub = json.load(open(os.path.join(base,"running_re_sub.jsonc"),'r'))
            for pattern, repl in running_re_sub.items():
                info = re.sub(pattern,repl,info)
            if SbyS_trans:
                info = re.sub(r'[\?\!。？！] *',lambda x:x.group()+'\n\n',info)
                info = re.sub(r' *\. *','.',info)
                info = re.sub(r'\.[^0-9,.\[\]][^,.]',lambda x:'.\n\n'+x.group()[-2:],info)
                info = info.replace('. ','.\n\n')
            Trans_End = False
            self.copy['text'] = 'Translating...'
            self.processed_ori_info = info
            trans_call = TransThread(info)
            trans_call.start()
        self.show()

    def Tcopy(self):
        pyperclip.copy(self.textBoard['text'])

    def Tcopy_ori(self):
        pyperclip.copy(self.processed_ori_info)

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

        self.textBoard = tk.Label(self.app, text='', bg='white', width = 43, wraplength = 240, justify = 'left')
        self.textBoard.pack()
        self.copy = tk.Button(self.app, text="Copy", command=self.Tcopy, bg = "DeepSkyBlue", width=30, height=1)
        self.copy_ori = tk.Button(self.app, text="Ori-Text", command=self.Tcopy_ori, bg = "BurlyWood", width=12, height=1)
        self.copy.pack(side=tk.LEFT)
        self.copy_ori.pack(side=tk.LEFT)

        self.showTrans('')
        self.on_closing()
        self.app.mainloop()

def onKeyUp(event):
    global combineKey
    if event.Key is None: return True
    for key in combineKey.keys():
        if key in event.Key:
            combineKey[key] = 0
            return True
    return True

def onKeyDown(event):
    global combineKey
    if event.Key is None: return True
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
    with open(os.path.join(base,'setting.jsonc'),'r') as f:
        dic = json.load(f)
    name = ['translate','append','show']
    keys = [[checkList[x] if x in checkList else x for x in dic[n]] for n in name]
    windowThread = UIThread()
    func = [windowThread.translate,windowThread.appendText,windowThread.show]
    windowThread.start()
    hm = PyHook3.HookManager()
    hm.KeyDown = onKeyDown
    hm.KeyUp = onKeyUp
    hm.HookKeyboard()
    pythoncom.PumpMessages()
