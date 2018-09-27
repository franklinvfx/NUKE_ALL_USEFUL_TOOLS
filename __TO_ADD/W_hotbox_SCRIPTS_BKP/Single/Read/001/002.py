#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Mocha
#
#----------------------------------------------------------------------------------------------------------

from cgev.common import environment
from cgev.common import system
import os
#import win32gui
 
def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

mocha_path = 'C:/Program Files/Imagineer Systems Ltd/mocha Pro V5/bin/mochapro.exe'
if os.path.exists(mocha_path):
    mocha_path = "\"C:\\Program Files\\Imagineer Systems Ltd\\mocha Pro V5\\bin\\mochapro.exe\" "
else:
    mocha_path = environment.getBinPath().replace('\\', '//')+'/mochaProV2/bin/mochapro.exe '

filename = nuke.selectedNode().knob('file').value()
filename = filename.split('.')
size = len(filename[-2])
filename[-2] = str(nuke.selectedNode().firstFrame()).zfill(size)
filename = '.'.join(filename)

system.shell([mocha_path + filename], mode=system.EXEC_MODE.BACKGROUND)