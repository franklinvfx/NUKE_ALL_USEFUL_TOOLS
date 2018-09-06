#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Invert Mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('invertmask').value() == 0:
	    i.knob('invertmask').setValue(1)
	    i.knob('icon').setValue('//stora/diska/global/templatesProd/Other_images/invert.png')
	else:
	    i.knob('invertmask').setValue(0)
	    i.knob('icon').setValue(' ')