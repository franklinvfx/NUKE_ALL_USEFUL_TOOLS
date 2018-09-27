#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Alpha/rgb/All
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('channels').value() == 'alpha':
        i.knob('channels').setValue('rgb')
    elif i.knob('channels').value() == 'rgb':
        i.knob('channels').setValue('all')
    else:
        i.knob('channels').setValue('alpha')