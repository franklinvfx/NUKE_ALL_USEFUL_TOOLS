#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Reduce Gain
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('gain').setValue(0.1 * i.knob('gain').value())