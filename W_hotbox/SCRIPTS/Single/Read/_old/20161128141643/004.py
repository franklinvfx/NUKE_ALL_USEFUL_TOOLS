#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: To nearest frame
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.allNodes('Read'):
	node.knob('on_error').setValue('nearest frame')