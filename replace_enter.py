import pyperclip
import sys,os
import json
import re
import PyHook3
import pythoncom
import win32api,win32gui
from time import time

last = None
if len(sys.argv)==1:
    ct = win32api.GetConsoleTitle()
    hd = win32gui.FindWindow(0, ct)
    win32gui.ShowWindow(hd, 0)
    with open('stop_replace.bat','w') as f:
        f.write('taskkill /pid {} /f\n'.format(os.getpid()))
        f.write('del %0')

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

def rep():
    global last
    info = pyperclip.paste()
    info = info.replace('\n','').replace('\r','')
    last = info
    pyperclip.copy(info)

def line():
    global last
    info = pyperclip.paste()
    info = info.replace('\n','').replace('\r','')
    info = re.sub(r'[\?\!。？！] *',lambda x:x.group()+'\n\n',info)
    def func(m): return m.group()[0]+'\n\n'+m.group()[-1]*(m.group()[-1]!=' ')
    info = re.sub('\. *[^0-9,]',func,info)
    last = info
    pyperclip.copy(info)

def app():
    global last
    info = pyperclip.paste()
    last = last+' '+info
    pyperclip.copy(last)

if __name__ == '__main__':
    base = sys.path[0]
    with open(os.path.join(base,'setting.json'),'r') as f:
        dic = json.load(f)
    name = ['translate','append']
    keys = [[checkList[x] if x in checkList else x for x in dic[n]] for n in name]
    func = [rep,line]
    hm = PyHook3.HookManager()
    hm.KeyDown = onKeyDown
    hm.KeyUp = onKeyUp
    hm.HookKeyboard()
    pythoncom.PumpMessages()