#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set to Frame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('reference_frame').setValue(nuke.frame())
	i.knob('label').setValue('RefFrame : [value reference_frame]')
