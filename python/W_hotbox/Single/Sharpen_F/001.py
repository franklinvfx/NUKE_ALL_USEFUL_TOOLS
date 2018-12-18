#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Invert mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('invertMask').value() == 0:
        i.knob('invertMask').setValue(1)
    else:
        i.knob('invertMask').setValue(0)