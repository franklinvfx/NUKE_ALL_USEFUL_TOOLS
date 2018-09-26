#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: End on current frame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('last').setValue(nuke.frame())
