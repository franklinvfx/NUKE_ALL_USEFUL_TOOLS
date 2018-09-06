#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set to frame
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
	node.knob('project_frame').setValue(nuke.frame())
