#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: IMask/Mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('Imask').value() == 0:
	    i.knob('Imask').setValue(1)
	else:
	    i.knob('Imask').setValue(0)