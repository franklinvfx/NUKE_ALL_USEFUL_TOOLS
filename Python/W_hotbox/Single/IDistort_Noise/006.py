#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: View Noise
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('ShowNoise').value() == 0:
	    i.knob('ShowNoise').setValue(1)
	else:
	    i.knob('ShowNoise').setValue(0)