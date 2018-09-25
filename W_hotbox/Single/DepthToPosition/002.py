#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Alpha/Rgb...
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('output').value() == 'alpha':
        i.knob('output').setValue('rgb')
        i.knob('label').setValue('(rgb)')
    elif i.knob('output').value() == 'rgb':
        i.knob('output').setValue('rgba')
        i.knob('label').setValue('(rgba)')
    else:
        i.knob('output').setValue('alpha')
        i.knob('label').setValue('')
    #messages.splash('Output set to : {}'.format(i.knob('output').value()))
