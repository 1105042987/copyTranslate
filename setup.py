import os 
import os.path as p
import sys

base = p.dirname(p.abspath(__file__))

if len(sys.argv)>1 and sys.argv[1] == 'install':
    os.system('python -m pip install --upgrade pip')
    os.system('pip install pyperclip PyExecJS')
    os.system('pip install '+p.join(base,'PyHook3-1.6.1-cp37-cp37m-win_amd64.whl'))

with open(p.join(base,'start.bat'),'w') as f:
    f.write('CALL '+ p.join(sys.path[4],'Scripts','activate.bat')+' '+sys.path[4]+'\n')
    f.write('start '+p.join(sys.path[4],'python')+' '+p.join(base,'copyTranslate.py'))
