#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Crop/UnCrop
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('crop').value() == 0:
	    i.knob('crop').setValue(1)
	else:
	    i.knob('crop').setValue(0)
