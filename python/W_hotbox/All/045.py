#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: delete selected
#
#----------------------------------------------------------------------------------------------------------

node = nuke.selectedNodes()

for n in node:
    nuke.delete(n)