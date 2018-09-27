#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: All/rgb
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	channelKnob = i.knob('channels')
	if channelKnob.value() == 'rgb':
		channelKnob.setValue('all')
	else:
		channelKnob.setValue('rgb')