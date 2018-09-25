#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: FTrack
#
#----------------------------------------------------------------------------------------------------------

from cgev.pipeline.appconnector.connectornuke import nukeMenu

mH = nukeMenu.MenuHandler()
mH.jumpToServer()

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