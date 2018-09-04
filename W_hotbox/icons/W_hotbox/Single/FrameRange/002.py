#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Jump to last frame
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
	nuke.frame(node.knob('last_frame').value())