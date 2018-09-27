#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: -25
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('numpixels').setValue(i.knob('numpixels').value()-25)