#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: P/N channels
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('P_channel').setValue('position')
	i.knob('N_channel').setValue('normals')