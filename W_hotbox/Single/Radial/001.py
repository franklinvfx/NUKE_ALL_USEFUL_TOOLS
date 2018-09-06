#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set to format
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    inputNode = i.input(0)
    i.knob('area').setValue((0,0,inputNode.width(),inputNode.height()))