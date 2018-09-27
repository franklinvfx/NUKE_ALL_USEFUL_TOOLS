#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Despill Green
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('expr0').setValue('')
	i.knob('expr1').setValue('g>(r+b)/2?(r+b)/2:g')
	i.knob('expr2').setValue('')
	i.knob('expr3').setValue('')
	i.knob('label').setValue('Despill Green')
	i.knob('tile_color').setValue(12517631)