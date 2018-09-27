#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Mocha
#
#----------------------------------------------------------------------------------------------------------

from cgev.common import environment
from cgev.common import system
#import win32gui
 
dirPath = nuke.selectedNode().knob('file').value()
dirPath = dirPath.split('/')[0:-1]
dirPath = '/'.join(dirPath)

if os.path.isdir(dirPath):
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    mocha_path = environment.getBinPath().replace('\\', '//')+'/mochaProV2/bin/mochapro.exe'
    
    filename = nuke.selectedNode().knob('file').value()
    filename = filename.split('.')
    size = len(filename[-2])
    filename[-2] = str(nuke.selectedNode().firstFrame()).zfill(size)
    filename = '.'.join(filename)
    
    system.shell(mocha_path+' '+filename, mode=system.EXEC_MODE.BACKGROUND)
else:
    nuke.message('You have to batch your shot before you can open it !')