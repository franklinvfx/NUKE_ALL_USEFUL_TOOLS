#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Horizontal
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('Horizontal'). value() == 0:
        i.knob('Horizontal'). setValue(1)
    else:
        i.knob('Horizontal').setValue(0)