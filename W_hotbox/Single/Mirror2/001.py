#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Flip
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('flip').setValue(1-i.knob('flip').value())