#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Alpha/Rgb...
#
#----------------------------------------------------------------------------------------------------------

saveValue = None

for i in nuke.selectedNodes():
    if saveValue is not None:
        i.knob('output').setValue(saveValue)
        i.knob('label').setValue('('+saveValue+')')
        if saveValue in ['alpha', 'all']:
            i.knob('label').setValue('')
    else:
        if i.knob('output').value() == 'alpha':
            i.knob('output').setValue('rgb')
            i.knob('label').setValue('(rgb)')
        elif i.knob('output').value() == 'rgb':
            i.knob('output').setValue('rgba')
            i.knob('label').setValue('(rgba)')
        elif i.knob('output').value() == 'rgba':
            i.knob('output').setValue('all')
            i.knob('label').setValue('')
        else:
            i.knob('output').setValue('alpha')
            i.knob('label').setValue('')
        saveValue = i.knob('output').value()
#    messages.splash('Channels set to : {}'.format(i.knob('channels').value()))