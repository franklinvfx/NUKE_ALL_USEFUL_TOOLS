#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set To Frame
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
	node.knob('RefFrame').setValue(nuke.frame())
