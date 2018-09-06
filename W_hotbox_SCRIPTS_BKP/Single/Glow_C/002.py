#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Effect Only
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('previewPost').value() == 0:
	    i.knob('previewPost').setValue(1)
	else:
	    i.knob('previewPost').setValue(0)