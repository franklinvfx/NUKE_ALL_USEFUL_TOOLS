#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set to frame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('reference_frame').setValue(nuke.frame())