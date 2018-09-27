#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Invert mask
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
    if i.knob('invert_mask').value() == 0:
        i.knob('invert_mask').setValue(1)
    else:
        i.knob('invert_mask').setValue(0)
        i.knob('icon').setValue(' ')
#messages.splash('Invert mask set to : {}'.format(i.knob('invert_mask').value()))