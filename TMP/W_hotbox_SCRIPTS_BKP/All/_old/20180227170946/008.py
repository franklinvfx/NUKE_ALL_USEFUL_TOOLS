#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create OCIOColorspaces
#
#----------------------------------------------------------------------------------------------------------

def main():
    if 'aces' in nuke.root().knob('OCIO_config').value():
        if len(nuke.selectedNodes()) == 0:
            nuke.message('Select a node to surround')
            return
        saveNode = nuke.selectedNode()
        dependent = saveNode.dependent()
        upperNode = saveNode.input(0)
    
        for node in nuke.selectedNodes():
            node.setSelected(False)
    
        colorSpaceInName = 'colorspaceIn'
        colorSpaceOutName = 'colorspaceOut'
        workingSpace = nuke.root().knob('workingSpaceLUT').value()
        logAlias = 'Aliases/logc3ei800_arriwide'
    
        colorSpaceIn = nuke.createNode('OCIOColorSpace',
                                       'in_colorspace ' + 'Aliases/' + workingSpace +
                                       ' out_colorspace ' + logAlias +
                                       ' name ' + colorSpaceInName, False)
        colorSpaceIn.setSelected(False)
        colorSpaceIn.setXYpos(saveNode.xpos(), saveNode.ypos()-35)
    
        colorSpaceOut = nuke.createNode('OCIOColorSpace',
                                        'in_colorspace ' + logAlias +
                                        ' out_colorspace ' + 'Aliases/' + workingSpace +
                                        ' name ' + colorSpaceOutName,
                                        False)
        colorSpaceOut.setSelected(False)
        colorSpaceOut.setXYpos(saveNode.xpos(), saveNode.ypos()+50)

        for node in dependent:
            if node.input(0) == saveNode:
                node.setInput(0, colorSpaceOut)
            elif node.input(1) is not None and node.input(1) == saveNode:
                node.setInput(1, colorSpaceOut)

        colorSpaceIn.setInput(0, upperNode)
        saveNode.setInput(0, colorSpaceIn)
        colorSpaceOut.setInput(0, saveNode)
        nuke.activeViewer().node().setInput(0, colorSpaceOut)
    else:
        nuke.message('This is only available when working in OCIO')
main()