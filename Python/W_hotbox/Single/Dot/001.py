#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: go to Input
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	prev = i.input(0)
	nuke.zoom( 1, [ prev.xpos(), prev.ypos() ])