#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set framerange
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('first').setValue(int(nuke.Root().knob('first_frame').value()))
	i.knob('last').setValue(int(nuke.Root().knob('last_frame').value()))