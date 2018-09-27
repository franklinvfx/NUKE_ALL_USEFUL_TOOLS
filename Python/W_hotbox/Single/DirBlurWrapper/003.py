#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Linear Blur
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('BlurType').setValue('linear')