#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: IMask/Mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('MaskMode').value() == 'IMask':
	    i.knob('MaskMode').setValue('Classic')
	else:
	    i.knob('MaskMode').setValue('IMask')