#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Over/Matte
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('output').setValue('rgba')
	if i.knob('operation').value() != 'over':
	    i.knob('operation').setValue('over')
	else:
	    i.knob('operation').setValue('matte')
'''
for i in nuke.selectedNodes():
    if i.knob('Achannels').value() == 'alpha':
        i.knob('Achannels').setValue('rgb')
        i.knob('Bchannels').setValue('rgb')
        i.knob('label').setValue('(rgb)')
        i.knob('also_merge').setValue('none')
    elif i.knob('Achannels').value() == 'rgb':
        i.knob('Achannels').setValue('rgba')
        i.knob('Bchannels').setValue('rgba')
        i.knob('label').setValue('(rgba)')
        i.knob('also_merge').setValue('none')
    elif i.knob('Achannels').value() == 'rgba':
        i.knob('Achannels').setValue('rgba')
        i.knob('Bchannels').setValue('rgba')
        i.knob('also_merge').setValue('all')
        i.knob('label').setValue('')       
    else:
        i.knob('Achannels').setValue('alpha')
        i.knob('Bchannels').setValue('alpha')
        i.knob('also_merge').setValue('none')
        i.knob('label').setValue('')'''