#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Alpha/Rgb...
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
    if i.knob('channels').value() == 'alpha':
        i.knob('channels').setValue('rgb')
        i.knob('label').setValue('(rgb)')
    elif i.knob('channels').value() == 'rgb':
        i.knob('channels').setValue('rgba')
        i.knob('label').setValue('(rgba)')
    elif i.knob('channels').value() == 'rgba':
        i.knob('channels').setValue('all')
        i.knob('label').setValue('')
    else:
        i.knob('channels').setValue('alpha')
        i.knob('label').setValue('')
    #messages.splash('Channels set to : {}'.format(i.knob('channels').value()))
