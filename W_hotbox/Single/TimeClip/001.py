#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Start on current frame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('first').setValue(nuke.frame())
