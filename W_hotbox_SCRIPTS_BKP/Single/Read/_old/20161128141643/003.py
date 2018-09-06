#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: To checkerboard
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.allNodes('Read'):
	node.knob('on_error').setValue('checkerboard')