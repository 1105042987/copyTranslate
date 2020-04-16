import pyperclip
import time
import os
import win32api
import win32gui
from googleTrans import translate
from GUI import show

ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0, ct)
win32gui.ShowWindow(hd, 0)

last=None
first = True
with open('stop.bat','w') as f:
    f.write('taskkill /pid {} /f\n'.format(os.getpid()))
    f.write('del %0')

while True:
    time.sleep(0.3)
    if pyperclip.paste()!=last:
        last = pyperclip.paste()
        if first:
            first = False
            continue
        if len(last)==0: continue
        trans = last.replace('\n',' ').replace('\r',' ')#.replace('. ','.\n')
        trans = translate(trans,oriLan='en')
        show(trans)
        # pyperclip.copy(last)