#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Combine RGB
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('expr0').setValue('')
	i.knob('expr1').setValue('')
	i.knob('expr2').setValue('')
	i.knob('expr3').setValue('clamp(r+g+b)')
	i.knob('label').setValue('RGB to Alpha')
	i.knob('tile_color').setValue(4278124287)