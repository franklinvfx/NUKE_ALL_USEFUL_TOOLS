#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Publish
# COLOR: #1fff00
# TEXTCOLOR: #000000
#
#----------------------------------------------------------------------------------------------------------

from cgev.ui import messages
from cgev.pipeline.data import session
from cgev.pipeline.appconnector import dialogOpener

sContext = session.getContext()
sManager = session.getManager()
element = nuke.selectedNodes()

dialogOpener.openDialogPublishImages(sManager, sContext, element)