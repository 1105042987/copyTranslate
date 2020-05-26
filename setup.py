import os 
import os.path as p
import sys

if len(sys.argv)>1 and sys.argv[1] == 'install':
    os.system('python -m pip install --upgrade pip')
    os.system('conda install swig')
    os.system('pip install pyperclip PyExecJS PyHook3')

base = p.dirname(p.abspath(__file__))
with open(p.join(base,'start.bat'),'w') as f:
    f.write('start '+p.join(sys.path[4],'python')+' '+p.join(base,'copyTranslate.py'))
