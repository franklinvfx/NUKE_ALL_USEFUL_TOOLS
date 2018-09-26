#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Alpha/Rgb...
#
#----------------------------------------------------------------------------------------------------------

from cgev.ui import messages
saveValue = None

for i in nuke.selectedNodes():
    if saveValue is not None:
        i.knob('channels').setValue(saveValue)
        i.knob('label').setValue('('+saveValue+')')
        if saveValue in ['alpha', 'all']:
            i.knob('label').setValue('')
    else:
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
        saveValue = i.knob('channels').value()
#    messages.splash('Channels set to : {}'.format(i.knob('channels').value()))