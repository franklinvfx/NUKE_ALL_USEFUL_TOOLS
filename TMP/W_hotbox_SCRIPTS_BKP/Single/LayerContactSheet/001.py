#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show layer names
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('showLayerNames').value() == 0:
	    i.knob('showLayerNames').setValue(1)
	else:
	    i.knob('showLayerNames').setValue(0)