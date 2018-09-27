#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Font -
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('note_font_size').setValue(i.knob('note_font_size').value()-10)