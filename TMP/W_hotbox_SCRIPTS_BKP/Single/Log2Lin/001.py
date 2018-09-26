#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Log2Lin/Lin2Log
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	if i.knob('operation').value() == 'log2lin':
	    i.knob('operation').setValue('lin2log')
	else:
	    i.knob('operation').setValue('log2lin')