#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Lum On/Off
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
    if i.knob('MixLuminance'). value() == 0:
        i.knob('MixLuminance'). setValue(1)
    else:
        i.knob('MixLuminance').setValue(0)
    #messages.splash('Luminance set to : {}'.format(i.knob('MixLuminance').value()))