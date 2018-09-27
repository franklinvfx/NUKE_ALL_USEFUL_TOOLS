#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Next Input
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('which').setValue( min( (i.knob('which').value() + 1),  (i.inputs() - 1)) )