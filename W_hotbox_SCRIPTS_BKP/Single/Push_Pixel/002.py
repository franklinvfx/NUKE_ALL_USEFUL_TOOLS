#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Alpha Mode
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('matte').value() == 'From Source':
	    i.knob('matte').setValue('Create New Input')
	else:
	    i.knob('matte').setValue('From Source')