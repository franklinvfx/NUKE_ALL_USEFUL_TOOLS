#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: BBox Union/B
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('bbox').setValue(1-int(i.knob('bbox').getValue()))
