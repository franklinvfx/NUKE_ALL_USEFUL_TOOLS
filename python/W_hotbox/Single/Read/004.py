#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Frame range hold/black
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.allNodes('Read'):
    if node.knob('before').value() != 'hold':
        node.knob('before').setValue('hold')
        node.knob('after').setValue('hold')
    else:
        node.knob('before').setValue('black')
        node.knob('after').setValue('black')