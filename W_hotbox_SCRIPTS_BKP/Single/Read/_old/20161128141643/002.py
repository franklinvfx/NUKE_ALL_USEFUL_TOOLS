#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: To error
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.allNodes('Read'):
	node.knob('on_error').setValue('error')