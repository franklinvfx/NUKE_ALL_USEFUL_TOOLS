#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set to 0
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('value').setValueAt(0,nuke.frame())
