#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: + 1 Stops
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('gang').value() == 1:
		i.knob('mode').setValue('Stops')
		i.knob('red').setValue(i.knob('red').value()+1)
	else : 
		i.knob('mode').setValue('Stops')
		i.knob('red').setValue(i.knob('red').value()+1)
		i.knob('green').setValue(i.knob('green').value()+1)
		i.knob('blue').setValue(i.knob('blue').value()+1)