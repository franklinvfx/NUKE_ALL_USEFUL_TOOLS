#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Keep RGBA
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('operation').setValue('keep')
	i.knob('channels').setValue('rgba')