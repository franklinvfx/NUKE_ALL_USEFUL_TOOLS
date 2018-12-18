#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: No Tesselation
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('rows').setValue('1')
	i.knob('columns').setValue('1')