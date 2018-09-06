#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Cubic/Simon
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
	if i.knob('filter').value() == 'Cubic':
	    i.knob('filter').setValue('Simon')
	else:
	    i.knob('filter').setValue('Cubic')
#messages.splash('Filter set to : {}'.format(i.knob('filter').value()))