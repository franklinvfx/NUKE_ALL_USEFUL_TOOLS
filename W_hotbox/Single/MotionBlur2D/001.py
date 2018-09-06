#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: VectorBlur
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()

def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

for i in selection:
	emptySelection(selection)
	i.knob('selected').setValue(True)
	nuke.createNode('VectorBlur2').knob('uv').setValue('motion')
