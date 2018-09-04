#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: RV <font color = "grey"> (Shift+Alt+F)
#
#----------------------------------------------------------------------------------------------------------

from cgev.nuke.tools import flipbook

dirPath = nuke.selectedNode().knob('file').value()
dirPath = dirPath.split('/')[0:-1]
dirPath = '/'.join(dirPath)

if os.path.isdir(dirPath):
    first = nuke.Root()['first_frame'].value()
    last = nuke.Root()['last_frame'].value()
    
    nuke.selectedNode().knob('reading').setValue(True)
    nuke.selectedNode().knob('use_limit').setValue(True)
    nuke.selectedNode().knob('first').setValue(first)
    nuke.selectedNode().knob('last').setValue(last)
    
    flipbook.openFlipBookRV(nuke.selectedNode())
    
    nuke.selectedNode().knob('reading').setValue(False)
    nuke.selectedNode().knob('use_limit').setValue(False)
    nuke.selectedNode().knob('postage_stamp').setValue(False)
else:
    nuke.message('You have to batch your shot before you can open it !')