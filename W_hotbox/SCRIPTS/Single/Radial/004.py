#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: rgba/alpha
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	channelKnob = i.knob('output')
	if channelKnob.value() == 'rgba':
		channelKnob.setValue('alpha')
	else:
		channelKnob.setValue('rgba')