#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Boost Gain
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('gain').setValue(10 * i.knob('gain').value())