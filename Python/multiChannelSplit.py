#################################################################
#  MultiChannelSplit
#
#  @author simon jokuschies
#  @email info@leafpictures.de
#  @version 3.0
#
#  description:
#  the script splits a multichannel exr into single layers
#  and autocrops them automatically.
#
#  instalation
#
#  put whole MultiChannelSplit folder in nuke home directory
#  in your init.py write this lines (without #) :
#
#  nuke.pluginAddPath("MultiChannelSplit")
#
#################################################################

# No need to change anything from here.
# Edit only if you exactly know what you're doing.

import nuke
import nukescripts
import os


def getUniqueChannelLayerList(readNode):
    '''
    return all channel layer that are included in the selected read node
    return: string-array
    '''
    # Function that returns unique channel layers
    rawChannelList = readNode.channels()
    channelLayerList = []
    for channel in rawChannelList:
        channelLayer = channel.split(".")
        channelLayerList.append(channelLayer[0])

    channelLayerList = list(set(channelLayerList))
    channelLayerList.sort()
    return channelLayerList


def createFolders(path):
    '''
    create folder if not exist
    return true if suceeded, false otherwise
    '''
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
            print "created dir at %s" % path
            return True
        except:
            print "could not created dir at %s" % path
            return False


class MultiChannelSplitPanel(nukescripts.PythonPanel):
    '''
    MultiChannelSplitPanel
    '''
    def __init__(self):
            '''
            init values
            '''
            global uniqueLayers
            global layerCheckboxes
            global panelHeight

            panelHeight = 160

            nukescripts.PythonPanel.__init__(self,
                                             "MultichannelSplit",
                                             "MultiChannelSplit")
            self.setMinimumSize(450, panelHeight)

            self.autoCrop = nuke.Boolean_Knob("autoCrop",
                                              "autocrop", 0.0)
            self.autoCrop.setFlag(nuke.STARTLINE)
            self.prepareForOutput = nuke.Boolean_Knob("prepareForOutput",
                                                      "prepare for output",
                                                      0.0)
            self.prepareForOutput.setFlag(nuke.STARTLINE)
            self.outputPath = nuke.File_Knob('outputPath', 'output path')
            self.outputPath.setVisible(False)
            self.div = nuke.Text_Knob("", "", "")
            self.which = nuke.Enumeration_Knob("which", "",
                                               ["all AOVs", "individual AOVs"])
            self.addKnob(self.autoCrop)
            self.addKnob(self.prepareForOutput)
            self.addKnob(self.outputPath)
            self.addKnob(self.div)
            self.addKnob(self.which)

            # Layer checkboxes
            uniqueLayers = getUniqueChannelLayerList(nuke.selectedNode())
            layerCheckboxes = []
            self.allLayer = nuke.Script_Knob("allLayer", "select all")
            self.allLayer.setVisible(False)
            self.noLayer = nuke.Script_Knob("noLayer", "deselect all")
            self.noLayer.setVisible(False)
            self.div2 = nuke.Text_Knob("", "available AOVs", "")
            self.div2.setVisible(False)
            self.addKnob(self.div2)
            self.addKnob(self.allLayer)
            self.addKnob(self.noLayer)

            for layer in uniqueLayers:
                self.layer = nuke.Boolean_Knob(layer, layer, 0)
                self.layer.setFlag(nuke.STARTLINE)
                self.layer.setVisible(False)
                self.addKnob(self.layer)
                layerCheckboxes.append(self.layer)

            self.div3 = nuke.Text_Knob("", "", "")
            self.addKnob(self.div3)

    def show(self):
        '''
        action performed when pressed ok
        '''
        if nukescripts.PythonPanel.showModalDialog(self):

            def multiChannelSplit():
                '''
                main function
                split the selected read node in separate channel layers
                if set create separate folders and write nodes
                '''
                sel = nuke.selectedNode()

                shuffles = []
                renderTo = ""
                autocropNodeRGB_exists = False
                cropNode = None
                dot = None

                if sel is not None:
                    # Main procedure
                    # Create shuffle, shuffle channel in, curvetool crop
                    # Create cropnode and paste that information in
                    # Delete crop node
                    o = 0
                    if self.autoCrop.getValue() == 1.0:
                        curveName = 'Autocrop_Master'
                        curveNode = nuke.nodes.CurveTool(name=curveName,
                                                         inputs=[sel],
                                                         operation="Auto Crop")
                        curveNode["channels"].setValue("rgba")
                        curveNode.knob("ROI").setValue([0, 0,
                                                        sel.width(),
                                                        sel.height()])
                        nuke.execute(curveNode, sel.knob("first").value(),
                                     sel.knob("last").value())

                    layersToProcess = []
                    if self.which.getValue() == 0.0:
                        layersToProcess = uniqueLayers
                    else:
                        for layer in layerCheckboxes:
                            if layer.getValue() is True:
                                layersToProcess.append(layer.name())

                    if len(layersToProcess) > 0:
                        dot = nuke.createNode("Dot", inpanel=False)

                        for channelLayer in layersToProcess:
                            shuffleName = "Shuffle_" + channelLayer
                            shuffleNode = nuke.nodes.Shuffle(name=shuffleName)
                            shuffles.append(shuffleNode.name())
                            shuffleNode.knob("in").setValue(channelLayer)
                            shuffleNode["hide_input"].setValue(True)
                            shuffleNode.setInput(0, sel)

                            xpos = sel["xpos"].getValue() + (o*100)
                            ypos = sel["ypos"].getValue() + 150
                            shuffleNode["xpos"].setValue(xpos)
                            shuffleNode["ypos"].setValue(ypos)
                            shuffleNode.setInput(0, dot)
                            shuffleNode["postage_stamp"].setValue(True)

                            # Auto crop if selected
                            if self.autoCrop.getValue() == 1.0:
                                if autocropNodeRGB_exists is False:
                                    cropNode = nuke.nodes.Crop(name=channelLayer, inputs=[shuffleNode])
                                    cropNode.knob("hide_input").setValue(True)
                                    cropNode.knob("box").copyAnimations(curveNode.knob("autocropdata").animations())
                                    nuke.delete(curveNode)
                                    cropNode.knob("postage_stamp").setValue(True)

                                    xpos = int(shuffleNode["xpos"].getValue())
                                    ypos = shuffleNode["ypos"].getValue()+80
                                    ypos = int(ypos)
                                    cropNode.setXpos(xpos)
                                    cropNode.setYpos(ypos)
                                    shuffleNode["hide_input"].setValue(False)
                                    cropNode["hide_input"].setValue(True)
                                    nukescripts.clear_selection_recursive()
                                    cropNode["selected"].setValue(True)
                                    nuke.nodeCopy("%clipboard%")
                                    autocropNodeRGB_exists = True
                                    shuffleNode["postage_stamp"].setValue(False)
                                    cropNode["postage_stamp"].setValue(True)
                                else:
                                    cropCopy = nuke.nodePaste("%clipboard%")
                                    cropCopy["name"].setValue(channelLayer)
                                    cropCopy.setInput(0, shuffleNode)

                                    xpos = int(shuffleNode["xpos"].getValue())
                                    ypos = shuffleNode["ypos"].getValue()+80
                                    ypos = int(ypos)
                                    cropCopy.setXpos(xpos)
                                    cropCopy.setYpos(ypos)

                            # Create folders for all layer and
                            # Create write node for every shuffle
                            if self.outputPath.getValue() != "":
                                renderTo = self.outputPath.getValue()
                                # CreateFolder
                                createFolders(renderTo+"/"+channelLayer)
                                # Create write node
                                write = nuke.nodes.Write()
                                write.knob("file_type").setValue("exr")

                                fileValue = renderTo + channelLayer
                                fileValue += '/' + channelLayer + "_%04d.exr"
                                write.knob("file").setValue(fileValue)

                                cValue = "Zip (16 scanlines)"
                                write.knob("compression").setValue(cValue)
                                write.knob("channels").setValue("rgba")

                                if self.autoCrop.getValue() is True:
                                    write.setInput(0, cropNode)
                                else:
                                    write.setInput(0, shuffleNode)
                            o += 1

                    if len(layersToProcess) > 0:
                        nuke.delete(dot)

                    # Hide all created shuffle inputs
                    for shuffleNode in shuffles:
                        if self.autoCrop.getValue() == 1.0:
                            temp = nuke.toNode(shuffleNode)
                            temp.knob("hide_input").setValue(True)
                            temp.knob("postage_stamp").setValue(True)
                else:
                    pass

            multiChannelSplit()

    def knobChanged(self, knob):
        '''
        panel knob changed actions
        '''
        if knob.name() == "prepareForOutput":
            if self.prepareForOutput.getValue() == 1.0:
                self.outputPath.setVisible(True)
                self.setMinimumSize(450, panelHeight+50)
            else:
                self.outputPath.setVisible(False)
                self.setMaximumSize(450, panelHeight)

        if knob.name() == "allLayer":
            for layer in layerCheckboxes:
                layer.setValue(1.0)

        if knob.name() == "noLayer":
            for layer in layerCheckboxes:
                layer.setValue(0.0)

        if knob.name() == "which":
            if self.which.getValue() == 1.0:
                self.setMinimumSize(450,
                                    panelHeight + (len(layerCheckboxes) * 25))
                self.allLayer.setVisible(True)
                self.noLayer.setVisible(True)
                self.div2.setVisible(True)
                for layer in layerCheckboxes:
                    layer.setVisible(True)
            else:
                self.setMaximumSize(450, panelHeight)
                self.setMinimumSize(450, panelHeight)
                self.allLayer.setVisible(False)
                self.noLayer.setVisible(False)
                self.div2.setVisible(False)
                for layer in layerCheckboxes:
                    layer.setVisible(False)


def MultiChannelSplit():
    '''
    execute main
    '''
    MultiChannelSplitPanel().show()
