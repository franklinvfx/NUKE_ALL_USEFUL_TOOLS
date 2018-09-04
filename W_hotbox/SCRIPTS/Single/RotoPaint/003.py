#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Output paint alpha
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
	node.knob('outputMask').setValue('rgba.alpha')