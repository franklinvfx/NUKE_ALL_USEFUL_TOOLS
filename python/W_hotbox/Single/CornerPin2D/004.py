#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Break "from" animation
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    #i.knob('copy_from_to').execute()
    i.knob('from1').clearAnimated()
    i.knob('from2').clearAnimated()
    i.knob('from3').clearAnimated()
    i.knob('from4').clearAnimated()
    i.knob('label').setValue('Match Frame : '+str(nuke.frame()))