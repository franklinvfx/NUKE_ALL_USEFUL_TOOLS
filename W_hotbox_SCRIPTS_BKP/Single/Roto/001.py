#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set lifetime to all
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
	node.knob('lifetime_type').setValue('all')