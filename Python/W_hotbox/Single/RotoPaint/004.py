#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Extract shapes
#
#----------------------------------------------------------------------------------------------------------

### to extract selected roto shapes from selected roto node
import copy
selNode = nuke.selectedNode()

if len(nuke.selectedNode().knob('curves').getSelected()) > 0:
    panel = nuke.Panel("extractSelectedShapes", 200)
    panel.addEnumerationPulldown('shapes goes to:\nroto node', 'single each')
    panel.addButton("cancel")
    panel.addButton("ok")
    showPanel = panel.show()
    userChoice = panel.value('shapes goes to:\nroto node')

    if showPanel == 1:
        if userChoice == 'single':
            newRotoNode = nuke.nodes.Roto(xpos=selNode.xpos()+200, ypos=selNode.ypos()-25)
            newRotoNode['curves'].rootLayer.setTransform(selNode['curves'].rootLayer.getTransform())

            for selShape in selNode['curves'].getSelected():
                newRotoNode.setName(selShape.name)
                newRotoNode['curves'].rootLayer.append(selShape.clone())
            newRotoNode.selectOnly()
            nuke.nodeCopy('%clipboard%')
            nuke.nodePaste('%clipboard%')
            nuke.delete(newRotoNode)
        else:
            xpos = 0
            for selShape in selNode['curves'].getSelected():
                xpos += 200
                newRotoNode = nuke.nodes.Roto(xpos=selNode.xpos()+xpos, ypos=selNode.ypos()-25)
                newRotoNode.setName(selShape.name)
                newRotoNode['curves'].rootLayer.setTransform(selNode['curves'].rootLayer.getTransform())
                newRotoNode['curves'].rootLayer.append(selShape.clone())
                newRotoNode.selectOnly()
                nuke.nodeCopy('%clipboard%')
                nuke.nodePaste('%clipboard%')
                nuke.delete(newRotoNode)
else:
    nuke.message('Select at least one shape to extract')
