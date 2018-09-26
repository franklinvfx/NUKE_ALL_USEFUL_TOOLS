#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: FTrack
#
#----------------------------------------------------------------------------------------------------------

import os
from cgev.pipeline.appconnector.connectornuke import nukeMenu

dirPath = nuke.selectedNode().knob('file').value()
dirPath = dirPath.split('/')[0:-1]
dirPath = '/'.join(dirPath)

if os.path.isdir(dirPath):
    mH = nukeMenu.MenuHandler()
    mH.jumpToServer()
else:
    nuke.message('You have to batch your shot before you can open it !')
'''from cgev.ui import messages
from cgev.pipeline.process import server
from cgev.pipeline.data import session
from cgev.common import jumping

sContext = session.getContext()

if not sContext.isEmpty():
    if session.getLockToServer():
        jumping.serverJump(server.getServerPath(),sContext.getTaskId())
    else:
        messages.info("Server is unlock.")
else:
    messages.info("Please, set your shot.")'''