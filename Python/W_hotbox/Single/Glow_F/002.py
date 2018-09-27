#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Effect Only
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('fxonly').value() == 0:
        i.knob('fxonly').setValue(1)
    else:
        i.knob('fxonly').setValue(0)