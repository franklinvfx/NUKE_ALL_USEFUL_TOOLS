#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Procedural/Input image
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('texture').value() == "Procedural":
	    i.knob('texture').setValue("Texture Input")
	else:
	    i.knob('texture').setValue("Procedural")