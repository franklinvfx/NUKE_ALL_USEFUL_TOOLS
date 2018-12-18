#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Render Textured/Off
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
	i.knob('label').setValue('render [value render_mode]')
	if i.knob('render_mode').value() == 'textured':
	    i.knob('render_mode').setValue('off')
	else:
	    i.knob('render_mode').setValue('textured')
#messages.splash('Render set to : {}'.format(i.knob('render_mode').value()))