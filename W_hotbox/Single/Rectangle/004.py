#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Replace On/Off
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	ReplaceKnob = i.knob('replace')
	if ReplaceKnob.value() == 1:
		ReplaceKnob.setValue(0)
	else:
		ReplaceKnob.setValue(1)