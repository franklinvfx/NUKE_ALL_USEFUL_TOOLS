#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create premult
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
	premult = nuke.createNode("Premult")
	node.setInput(0, premult)