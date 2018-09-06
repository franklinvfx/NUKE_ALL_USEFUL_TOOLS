#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create Read
#
#----------------------------------------------------------------------------------------------------------

from cgev.nuke.tools.nodes import write

filename = nuke.selectedNode()['file'].value()
write.createRead(filename)