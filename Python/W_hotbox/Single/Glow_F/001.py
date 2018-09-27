#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Invert Mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('disable_1').value() == 0:
        i.knob('disable_1').setValue(1)
    else:
        i.knob('disable_1').setValue(0)
        i.knob('icon').setValue(' ')