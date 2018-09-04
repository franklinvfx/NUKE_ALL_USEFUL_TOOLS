#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Size -
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('edge_size').setValue(i.knob('edge_size').value()-2)