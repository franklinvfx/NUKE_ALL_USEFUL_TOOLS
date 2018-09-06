#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Explorer <font color = "grey"> (Ctrl+R)
#
#----------------------------------------------------------------------------------------------------------

import os
from cgev.pipeline.appconnector.connectornuke import nukeMenu

dirPath = nuke.selectedNode().knob('file').value()
dirPath = dirPath.split('/')[0:-1]
dirPath = '/'.join(dirPath)

if os.path.isdir(dirPath):
    mH = nukeMenu.MenuHandler()
    mH.jumpToFile()
else:
    nuke.message('You have to batch your shot before you can open it !')