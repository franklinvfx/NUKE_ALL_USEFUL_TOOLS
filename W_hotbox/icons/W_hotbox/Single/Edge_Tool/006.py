#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Out Alpha/Rgba
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('ChannelOut').value() == "Alpha":
	    i.knob('ChannelOut').setValue("rgba")
	    i.knob('label').setValue("(rgba)")
	else:
	    i.knob('ChannelOut').setValue("Alpha")
	    i.knob('label').setValue("")