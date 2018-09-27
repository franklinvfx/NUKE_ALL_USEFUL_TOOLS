#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Vertical/Horizontal
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
	if i.knob('rotation').value() == 0:
	    i.knob('rotation').setValue(90)
	else:
	    i.knob('rotation').setValue(0)
#messages.splash('Angle set to : {}'.format(i.knob('rotation').value()))