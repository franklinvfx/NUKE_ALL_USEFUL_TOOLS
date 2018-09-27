#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show filter
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('label').value() == '[value amplitude] px at [value frequency]':
	    i.knob('label').setValue('[value amplitude] px at [value frequency] /[value filter]')
	else:
	    i.knob('label').setValue('[value amplitude] px at [value frequency]')