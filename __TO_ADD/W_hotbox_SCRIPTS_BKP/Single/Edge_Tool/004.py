#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Outside
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('edge_size').setValue(0)
    i.knob('erode_in').setValue(0)
    i.knob('erode_out').setValue(10)