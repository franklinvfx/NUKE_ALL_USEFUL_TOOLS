#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Invert mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('disable_1').value() == 0:
	    i.knob('disable_1').setValue(1)
	    i.knob('icon').setValue('//stora/diska/global/templatesProd/Other_images/invert.png')
	else:
	    i.knob('disable_1').setValue(0)
	    i.knob('icon').setValue(' ')