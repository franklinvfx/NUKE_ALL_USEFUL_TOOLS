#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Jump to frame
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
	nuke.frame(node.knob('first_frame').value())