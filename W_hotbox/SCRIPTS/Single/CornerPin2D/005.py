#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Break "to" animation
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('to1').clearAnimated()
    i.knob('to2').clearAnimated()
    i.knob('to3').clearAnimated()
    i.knob('to4').clearAnimated()
    i.knob('label').setValue('Stab Frame : '+str(nuke.frame()))