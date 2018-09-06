#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set to 1
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('value').setValueAt(1,nuke.frame())
