#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: BBox Union/B
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
	i.knob('bbox').setValue(1-int(i.knob('bbox').getValue()))
#messages.splash('BBox set to : {}'.format(i.knob('bbox').value()))
