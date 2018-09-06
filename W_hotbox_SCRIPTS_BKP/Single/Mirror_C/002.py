#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Vertical
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('Vertical'). value() == 0:
        i.knob('Vertical'). setValue(1)
    else:
        i.knob('Vertical').setValue(0)