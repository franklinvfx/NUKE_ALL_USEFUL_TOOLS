#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Missing frames error/black
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.allNodes('Read'):
    if node.knob('on_error').value() != 'black':
       node.knob('on_error').setValue('black')
    else:
        node.knob('on_error').setValue('error')