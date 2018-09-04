#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Cubic/Simon
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('vector_filter').value() == 'Cubic':
	    i.knob('vector_filter').setValue('Simon')
	else:
	    i.knob('vector_filter').setValue('Cubic')