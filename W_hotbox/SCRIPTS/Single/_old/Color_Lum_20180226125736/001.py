#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Color/Lum
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
	if i.knob('mode').value() == 'Color':
	    i.knob('mode').setValue('Luminosity')
	else:
	    i.knob('mode').setValue('Color')
#messages.splash('Keep set to : {}'.format(i.knob('mode').value()))