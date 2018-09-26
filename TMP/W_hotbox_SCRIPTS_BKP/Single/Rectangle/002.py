#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Hard/Smooth
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	softKnob = i.knob('softness')
	if softKnob.value() == 1:
		softKnob.setValue(0)
	else:
		softKnob.setValue(100)