#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Localize
#
#----------------------------------------------------------------------------------------------------------

def localize(nodes):

    for node in nodes:
        if node.knob('localizationPolicy').value() == 'off':
            node.knob('localizationPolicy').setValue(0)
        else:
            node.knob('localizationPolicy').setValue(2)

nodes = nuke.selectedNodes()
if len(nodes) > 1:
    if nuke.ask('Are you sure you want to modify all the selected Read nodes ?'):
        localize(nodes)
else:
    localize(nodes)