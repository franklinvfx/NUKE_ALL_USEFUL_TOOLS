#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show Size
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('label').value() == '':
	    i.knob('label').setValue('size : [value size]')
	else:
	    i.knob('label').setValue('')