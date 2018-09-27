#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Breakout Layers
#
#----------------------------------------------------------------------------------------------------------

def main():
    import nuke
    import nukescripts
    import os

    class shuffleChannels(nukescripts.PythonPanel):

        def __init__(self, n, folder):

            self.nukeFolder = folder
            nukescripts.PythonPanel.__init__(self, 'shuffle channels')
            self.n = n
            self.channels = self.n.channels()

            # Layers list builder
            self.layers = []
            for i in range(len(self.channels)):
                chanName = self.channels[i].split('.')[0]
                if chanName not in self.layers and 'rgba' not in chanName:
                    self.layers.append(chanName)

            # UI
            self.tabGroup = nuke.BeginTabGroup_Knob('tabGroup', '')
            self.addKnob(self.tabGroup)
            # Layers Tab
            self.layersTab = nuke.Tab_Knob('layersTab', 'channels')
            self.addKnob(self.layersTab)

            availableNodes = '%s (%s node)' % (self.n.name(), self.n.Class())
            self.selectedNodeName = nuke.Text_Knob('selectedNodeName',
                                                   'selected node: ',
                                                   availableNodes)
            self.addKnob(self.selectedNodeName)

            self.separator = nuke.Text_Knob('separator', '')
            self.addKnob(self.separator)

            self.presets = nuke.Enumeration_Knob('presets',
                                                 '', ['                   '])
            self.addKnob(self.presets)

            self.listLayers = []
            for i in range(len(self.layers)):
                layer = nuke.Boolean_Knob('layer'+str(i), str(self.layers[i]))
                layer.setValue(True)
                layer.setEnabled(False)
                self.addKnob(layer)
                layer.setFlag(4096)
                self.listLayers.append(layer)

            # Prefs Tab
            self.prefsTab = nuke.Tab_Knob('prefsTab', 'preferences')
            self.addKnob(self.prefsTab)

            self.text1 = nuke.Text_Knob('texte_separation',
                                        'generate')
            self.addKnob(self.text1)

            self.autocrop = nuke.Boolean_Knob('autocrop', 'Autocrop')
            self.addKnob(self.autocrop)
            self.autocrop.setFlag(4096)

            self.postage = nuke.Boolean_Knob('postage', 'Postage stamp')
            self.addKnob(self.postage)
            self.postage.setFlag(4096)

            self.remove = nuke.Boolean_Knob('remove', 'Remove node')
            self.addKnob(self.remove)
            self.remove.setFlag(4096)

            self.grade = nuke.Boolean_Knob('grade', 'Grade node')
            self.addKnob(self.grade)
            self.grade.setFlag(4096)

            self.noShuffLabel = nuke.Boolean_Knob('noShuffLabel',
                                                  'remove label from Shuffles')
            self.noShuffLabel.setValue(True)
            self.noShuffLabel.setFlag(4096)
            self.noShuffLabel.setVisible(False)
            self.addKnob(self.noShuffLabel)

            self.bdrop = nuke.Boolean_Knob('bdrop', 'Backdrop')
            self.addKnob(self.bdrop)
            self.bdrop.setFlag(4096)

            self.bdropColor = nuke.ColorChip_Knob('bdropColor',
                                                  'backDrop color')
            self.addKnob(self.bdropColor)
            self.bdropColor.setDefaultValue([926365441])

            self.text = nuke.Text_Knob('texte_separation',
                                       'separation between nodes')
            self.addKnob(self.text)

            self.separation = nuke.Double_Knob('separation',
                                               '')
            self.addKnob(self.separation)
            self.separation.setFlag(4096)
            self.separation.setRange(100, 400)
            self.separation.setDefaultValue([200])

            self.shuffLayersColor = nuke.ColorChip_Knob('shuffLayersColor',
                                                        'Shuffle color')
            self.addKnob(self.shuffLayersColor)
            prefNode = nuke.toNode('preferences')['NodeColour05Color'].value()
            self.shuffLayersColor.setDefaultValue([prefNode])

            self.EndTab = nuke.EndTabGroup_Knob('endTabGroup', '')
            self.addKnob(self.EndTab)

        def knobChanged(self, knob):
            if knob == self.presets:
                updateLayersPreset(self.nukeFolder)

        def returnLayers(self):
            return self.layers

        def returnChannels(self):
            return self.channels

    def getData(folder):
        # Gets selected node or not
        try:
            global n
            n = nuke.selectedNode()
        except:
            nuke.message('Select a node.')
            return

        rgbaSolo = True
        for channel in n.channels():
            if 'rgba' not in channel:
                rgbaSolo = False
                break

        if rgbaSolo:
            msg = 'There is only the rgba channel on this node.'
            nuke.message(msg)
            return
        else:
            global p
            # if all good, build and launches the panel
            p = shuffleChannels(n, folder)

        # Returns the layers list
        layers = p.returnLayers()

        # Changes panel dimensions
        windowHeight = len(layers)*20+165
        if windowHeight > 1000:
            windowHeight = 1000
        p.setMinimumSize(600, windowHeight)
        readPrefsFile(p, folder)
        refreshPresetsMenu(folder)

        # Launches the panel
        thePanel = p.showModalDialog()

        if thePanel is None or thePanel is False:
            return

        # Beyond this point all happens after the panel has been closed
        # Creation of the prefs variable
        prefs = {'remove': p.remove.value(),
                 'grade': p.grade.value(),
                 'noShuffLabel': p.noShuffLabel.value(),
                 'separation': p.separation.value(),
                 'shuffLayersColor': p.shuffLayersColor.value(),
                 'bdrop': p.bdrop.value(),
                 'bdropColor': p.bdropColor.value(),
                 'autocrop': p.autocrop.value(),
                 'postage': p.postage.value()}

        # Writes the preferences file
        writePrefsFile(p, str(prefs), folder)
        # Here I collect what layers have been selected
        layerList = []
        for i in range(len(layers)):
            gate = p.listLayers[i].value()
            if gate is True:
                layerList.append(layers[i])

        # Here it will create a node tree if some layers have been selected
        if len(layerList) > 0:
            buildTree(layerList, prefs)
        else:
            return

    def selectAll():
        for i in range(len(p.returnLayers())):
            p.listLayers[i].setValue(True)
            p.listLayers[i].setEnabled(False)

    def deselectAll():
        for i in range(len(p.returnLayers())):
            p.listLayers[i].setValue(False)
            p.listLayers[i].setEnabled(True)

    def buildTree(layers, prefs):
        n = nuke.selectedNode()
        nukePrefs = nuke.toNode('preferences')
        defGoofyFootValue = nukePrefs['goofy_foot'].value()
        nukePrefs['goofy_foot'].setValue(0)

        selNodeXPos = n.xpos()
        selNodeYPos = n.ypos()

        n.setSelected(False)

        shuffDot0 = nuke.createNode('Dot', 'selected False', False)
        shuffDot0YPos = int(selNodeYPos + 100)
        shuffDot0.setXYpos(int(selNodeXPos + 200), shuffDot0YPos)
        shuffDot0.setInput(0, n)

        # Creation of nodes
        listShuffDots = []
        for i in range(len(layers)):
            # Dots
            if i == 0:
                shuffDot = shuffDot0
            else:
                newXPos = (prefs['separation']*i)+shuffDot0.xpos()
                shuffDot = nuke.createNode('Dot', inpanel=False)
                shuffDot.setSelected(False)
                shuffDot.setXYpos(int(newXPos), shuffDot0YPos)
                shuffDot.setInput(0, listShuffDots[i-1])
            listShuffDots.append(shuffDot)

        # Shuffles
        save = nuke.toNode('preferences')['NodeColour05Color'].value()
        for i in range(len(layers)):
            newXPos = (prefs['separation']*i) + shuffDot0.xpos()
            setShuf = 'in %s ' % (layers[i])
            shuf = nuke.createNode('Shuffle', setShuf, False)
            shuf.setName(layers[i])
            shuf.setInput(0, listShuffDots[i])
            shuf.setXYpos(int(newXPos-34), shuffDot0YPos+50)

            # Color
            if prefs['shuffLayersColor'] != save:
                shuf['tile_color'].setValue(prefs['shuffLayersColor'])

            # Label
            if prefs['noShuffLabel'] == True:
                shuf['label'].setValue('')

            # Removes
            if prefs['remove'] == True:
                setRem = 'operation keep channels rgba selected False'
                rem = nuke.createNode('Remove', setRem, False)
                rem.setInput(0, shuf)

            # Grades
            if prefs['grade'] == True:
                nuke.createNode('Grade', inpanel=False)

            # Autocrop
            if prefs['autocrop']:
                nukescripts.autocrop()

            # Postage stamp
            if prefs['postage']:
                shuf.knob('postage_stamp').setValue(True)

            for node in nuke.selectedNodes():
                node.setSelected(False)

        # BackDrop
        width = 0
        height = 0
        if prefs['bdrop'] == True:
            width = (prefs['separation'] * (len(layers)))
            height = 350

            bd = nuke.createNode('BackdropNode',
                                 'tile_color %s' % (prefs['bdropColor']),
                                 inpanel=False)

            bd.setXYpos(int(shuffDot0.xpos() - 100), shuffDot0.ypos() - 100)
            bd['bdwidth'].setValue(width)
            bd['bdheight'].setValue(height)
            bd.setSelected(False)

        # Resets prefs to user defined state
        nukePrefs = nuke.toNode('preferences')
        nukePrefs['goofy_foot'].setValue(defGoofyFootValue)

    # Reads the preferences file and sets the values on the panel knobs
    def readPrefsFile(p, folder):
        try:
            prefsFileR = open(folder + 'BreakOutPrefs.txt', 'r')
        except:
            prefsFileW = open(folder + 'BreakOutPrefs.txt', 'w')
            prefsFileW.write("['prefs', {'All': ['All'], 'Selected':['Selected']}]")
            prefsFileW.close()
            return
        prefs = eval(prefsFileR.read())[0]
        for key in prefs:
            if key == 'remove':
                p.remove.setValue(prefs[key])
            elif key == 'grade':
                p.grade.setValue(prefs[key])
            elif key == 'noShuffLabel':
                p.noShuffLabel.setValue(prefs[key])
            elif key == 'separation':
                p.separation.setValue(prefs[key])
            elif key == 'shuffLayersColor':
                p.shuffLayersColor.setValue(prefs[key])
            elif key == 'bdrop':
                p.bdrop.setValue(prefs[key])
            elif key == 'bdropColor':
                p.bdropColor.setValue(prefs[key])
            elif key == 'autocrop':
                p.autocrop.setValue(prefs[key])
            elif key == 'postage':
                p.postage.setValue(prefs[key])

    def writePrefsFile(p, prefs, folder):
        prefsFile = open(folder + 'BreakOutPrefs.txt', 'r')
        prefsFileContent = eval(prefsFile.read())
        prefsFile.close()
        prefsFile = open(folder + 'BreakOutPrefs.txt', 'w')
        prefsFile.write("[%s, %s]" % (prefs, prefsFileContent[1]))

    def refreshPresetsMenu(folder):
        prefsFileR = open(folder + 'BreakOutPrefs.txt', 'r')
        prefsFileContent = eval(prefsFileR.read())
        presetsInFile = prefsFileContent[1]
        listPresets = sorted(presetsInFile.keys())
        listPresets.remove('Selected')
        listPresets.remove('All')
        listPresets.insert(0, 'Selected')
        listPresets.insert(0, 'All')
        p.presets.setValues(listPresets)

    def updateLayersPreset(folder):
        prefsFileR = open(folder + 'BreakOutPrefs.txt', 'r')
        prefsFileContent = eval(prefsFileR.read())
        presetsInFile = prefsFileContent[1]

        layersInPreset = presetsInFile[p.presets.value()]

        if p.presets.value() not in ['All', 'Selected']:
            for i in range(len(p.returnLayers())):
                lay = p.listLayers[i].label()
                if lay in layersInPreset:
                    p.listLayers[i].setValue(True)
        elif p.presets.value() == 'All':
            selectAll()
        else:
            deselectAll()
    getData(os.path.expanduser('~') + '/.nuke/')
main()
