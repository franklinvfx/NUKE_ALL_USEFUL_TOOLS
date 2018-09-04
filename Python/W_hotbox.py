#----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
version = '1.7'
releaseDate = 'June 26 2017'

#----------------------------------------------------------------------------------------------------------
#
#LICENSE
#
#----------------------------------------------------------------------------------------------------------

'''
Copyright (c) 2016, Wouter Gilsing
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Redistribution of this software in source or binary forms shall be free
      of all charges or fees to the recipient of this software.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

#----------------------------------------------------------------------------------------------------------

import nuke

#Choose between PySide and PySide2 based on Nuke version
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
else:
    from PySide2 import QtGui, QtCore, QtWidgets

import os
import subprocess
import platform

import traceback
import colorsys

import W_hotboxManager

preferencesNode = nuke.toNode('preferences')
operatingSystem = platform.system()

#----------------------------------------------------------------------------------------------------------

class hotbox(QtWidgets.QWidget):
    '''
    The main class for the hotbox
    '''

    def __init__(self, subMenuMode = False, path = '', name = '', position = ''):
        super(hotbox, self).__init__()

        self.active = True

        self.triggerMode = preferencesNode.knob('hotboxTriggerDropdown').getValue()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #enable transparency on Linux

        if operatingSystem not in ['Darwin','Windows']:
            self.setAttribute(QtCore.Qt.WA_PaintOnScreen)

        masterLayout = QtWidgets.QVBoxLayout()
        self.setLayout(masterLayout)

        self.selection = nuke.selectedNodes()


        #check whether selection in group
        self.groupRoot = 'root'

        if len(self.selection) != 0:
            nodeRoot = self.selection[0].fullName()
            if nodeRoot.count('.') > 0:
                self.groupRoot = '.'.join(nodeRoot.split('.')[:-1])

        self.activeButton = None

        #--------------------------------------------------------------------------------------------------
        #main hotbox
        #--------------------------------------------------------------------------------------------------

        if not subMenuMode:

            if len(self.selection) > 1:

                if len(list(set([i.Class() for i in nuke.selectedNodes()]))) == 1:
                    self.mode = 'Single'
                else:
                    self.mode = 'Multiple'

            else:
                self.mode = 'Single'

            #Layouts
            centerLayout = QtWidgets.QHBoxLayout()

            centerLayout.addStretch()
            centerLayout.addWidget(hotboxButton('Reveal in %s'%getFileBrowser(),'revealInBrowser()'))
            centerLayout.addSpacing(25)
            centerLayout.addWidget(hotboxCenter())
            centerLayout.addSpacing(25)
            centerLayout.addWidget(hotboxButton('Hotbox Manager','showHotboxManager()'))
            centerLayout.addStretch()

            self.topLayout = nodeButtons()
            self.bottomLayout = nodeButtons('bottom')
            spacing = 12

        #--------------------------------------------------------------------------------------------------
        #submenu
        #--------------------------------------------------------------------------------------------------

        else:

            allItems = [path + '/' + i for i in sorted(os.listdir(path)) if i[0] not in ['.','_']]

            centerItems = allItems[:2]

            lists = [[],[]]
            for index, item in enumerate(allItems[2:]):

                if int((index%4)/2):
                    lists[index%2].append(item)
                else:
                    lists[index%2].insert(0,item)


            #Stretch layout
            centerLayout = QtWidgets.QHBoxLayout()

            centerLayout.addStretch()
            for index, item in enumerate(centerItems):
                centerLayout.addWidget(hotboxButton(item))
                if index == 0:
                    centerLayout.addWidget(hotboxCenter(False,path))

            if len(centerItems) == 1:
                centerLayout.addSpacing(105)

            centerLayout.addStretch()

            self.topLayout = nodeButtons('SubMenuTop',lists[0])
            self.bottomLayout = nodeButtons('SubMenuBottom',lists[1])
            spacing = 0

        #--------------------------------------------------------------------------------------------------
        #Equalize layouts to make sure the center layout is the center of the hotbox
        #--------------------------------------------------------------------------------------------------

        difference = self.topLayout.count() - self.bottomLayout.count()

        if difference != 0:

            extraLayout = QtWidgets.QVBoxLayout()

            for i in range(abs(difference)):
                extraLayout.addSpacing(35)

            if difference > 0:
                self.bottomLayout.addLayout(extraLayout)
            else:
                self.topLayout.insertLayout(0,extraLayout)

        #--------------------------------------------------------------------------------------------------

        masterLayout.addLayout(self.topLayout)
        masterLayout.addSpacing(spacing)
        masterLayout.addLayout(centerLayout)
        masterLayout.addSpacing(spacing)
        masterLayout.addLayout(self.bottomLayout)

        #position
        self.adjustSize()

        self.spwanPosition = QtGui.QCursor().pos() - QtCore.QPoint((self.width()/2),(self.height()/2))

        #set last position if a fresh instance of the hotbox is launched
        if position == '' and not subMenuMode:
            global lastPosition
            lastPosition = self.spwanPosition

        if subMenuMode:
            self.move(self.spwanPosition)

        else:
            self.move(lastPosition)

        #make sure the widgets closes when it loses focus
        self.installEventFilter(self)

    def closeHotbox(self, hotkey = False):

        #if the execute on close function is turned on, the hotbox will execute the selected button upon close
        if hotkey:
            if preferencesNode.knob('hotboxExecuteOnClose').value():
                if self.activeButton != None:
                    self.activeButton.invokeButton()
                    self.activeButton = None

        self.active = False
        self.close()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return False
        if event.text() == shortcut:
            global lastPosition
            lastPosition = ''

            # if set to single tap, leave the hotbox open after launching, else close it.
            if not self.triggerMode:
                self.closeHotbox(hotkey = True)

            return True

    def keyPressEvent(self, event):
        if event.text() == shortcut:
            if event.isAutoRepeat():
                return False

            #if launch mode is set to 'Single Tap' close the hotbox.
            if self.triggerMode:
                self.closeHotbox(hotkey = True)
        else:
            return False

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate,QtCore.QEvent.FocusOut]:
            self.closeHotbox()
            return True
        return False

#----------------------------------------------------------------------------------------------------------
#Button field
#----------------------------------------------------------------------------------------------------------

class nodeButtons(QtWidgets.QVBoxLayout):
    '''
    Create QLayout filled with buttons
    '''
    def __init__(self, mode = '', allItems = ''):
        super(nodeButtons, self).__init__()

        selectedNodes = nuke.selectedNodes()
        mirrored = True

        #--------------------------------------------------------------------------------------------------
        #submenu
        #--------------------------------------------------------------------------------------------------

        if 'submenu' in mode.lower():

            self.rowMaxAmount = 3
            if 'top' in mode.lower():
                mirrored = False

        #--------------------------------------------------------------------------------------------------
        #main hotbox
        #--------------------------------------------------------------------------------------------------

        else:

            self.path = preferencesNode.knob('hotboxLocation').value().replace('\\','/')
            if self.path[-1] != '/':
                self.path = self.path + '/'

            self.allRepositories = list(set([self.path]+[i[1] for i in extraRepositories]))

            self.rowMaxAmount = int(preferencesNode.knob('hotboxRowAmountAll').value())

            self.folderList = []
            
            
            if mode == 'bottom':

                for repository in self.allRepositories:
                    self.folderList.append(repository + 'All/')

            else:
                mirrored = False
                self.rowMaxAmount = int(preferencesNode.knob('hotboxRowAmountSelection').value())

                nodeClasses = list(set([node.Class() for node in selectedNodes]))

                if len(nodeClasses) == 0:
                    nodeClasses = ['No Selection']

                else:

                    #check if group, if so take the name of the group, as well as the class
                    groupNodes = []
                    if 'Group' in nodeClasses:
                        for node in selectedNodes:
                            if node.Class() == 'Group':
                                groupName = node.name()
                                while groupName[-1] in [str(i) for i in range(10)]:
                                    groupName = groupName[:-1]
                                if groupName not in groupNodes and groupName != 'Group':
                                    groupNodes.append(groupName)

                    if len(groupNodes) > 0:
                        groupNodes = [nodeClass for nodeClass in nodeClasses if nodeClass != 'Group'] + groupNodes

                    if len(nodeClasses) > 1:
                        nodeClasses = [nodeClasses]
                    if len(groupNodes) > 1:
                        groupNodes = [groupNodes]

                    nodeClasses = nodeClasses + groupNodes

                '''
                Check which defined class combinations on disk are applicable to the current selection.
                '''

                for repository in self.allRepositories:
                    for nodeClass in nodeClasses:
                        if isinstance(nodeClass,list):

                            for managerNodeClasses in [i for i in os.listdir(repository + 'Multiple') if i[0] not in ['_','.']]:
                                managerNodeClassesList = managerNodeClasses.split('-')
                                match = list(set(nodeClass).intersection(managerNodeClassesList))

                                if len(match) >= len(nodeClass):
                                    self.folderList.append(repository + 'Multiple/' + managerNodeClasses)
                        else:
                            self.folderList.append(repository + 'Single/' + nodeClass)

            allItems = []

            self.folderList = list(set(self.folderList))
            for folder in self.folderList:
                #check if path exists
                if os.path.exists(folder):
                    for i in sorted(os.listdir(folder)):
                        if i[0] not in ['.','_'] and len(i) in [3,6]:
                            if folder[-1] != '/':
                                folder += '/'
                            allItems.append(folder + i)

        #--------------------------------------------------------------------------------------------------
        #devide in rows based on the row maximum

        allRows = []
        row = []

        for i in range(len(allItems)):
            currentItem = allItems[i]
            if preferencesNode.knob('hotboxButtonSpawnMode').value():
                if len(row) %2:
                    row.append(currentItem)
                else:
                    row.insert(0,currentItem)
            else:
                row.append(currentItem)
            #when a row reaches its full capacity, add the row to the allRows list
            #and start a new one. Increase rowcapacity to get a triangular shape
            if len(row) == self.rowMaxAmount:
                allRows.append(row)
                row = []
                self.rowMaxAmount += preferencesNode.knob('hotboxRowStepSize').value()

        #if the last row is not completely full, add it to the allRows list anyway
        if len(row) != 0:
            allRows.append(row)

        if mirrored:
            rows =  allRows
        else:
            rows =  allRows[::-1]

        #nodeHotboxLayout
        for row in rows:
            self.rowLayout = QtWidgets.QHBoxLayout()

            self.rowLayout.addStretch()

            for button in row:
                buttonObject = hotboxButton(button)
                self.rowLayout.addWidget(buttonObject)
            self.rowLayout.addStretch()

            self.addLayout(self.rowLayout)

        self.rowAmount = len(rows)

#----------------------------------------------------------------------------------------------------------

class hotboxCenter(QtWidgets.QLabel):
    '''
    Center button of the hotbox.
    If the 'color nodes' is set to True in the preferences panel, the button will take over the color and
    name of the current selection. If not, the button will be the same color as the other buttons will
    be in their selected state. The text will be read from the _name.json file in the folder.
    '''

    def __init__(self, node = True, name = ''):
        super ( hotboxCenter ,self ).__init__()

        self.node = node

        nodeColor = '#525252'
        textColor = '#eeeeee'

        selectedNodes = nuke.selectedNodes()

        if node:

            #if no node selected
            if len(selectedNodes) == 0:
                name = 'W_hotbox'
                nodeColorRGB = interface2rgb(640034559)

            #if node(s) selected
            else:
                name = nuke.selectedNode().name()
                nodeColorRGB = interface2rgb(getTileColor())

            if preferencesNode.knob('hotboxColorCenter').value():
                nodeColor = rgb2hex(nodeColorRGB)

                nodeColorHSV = colorsys.rgb_to_hsv(nodeColorRGB[0],nodeColorRGB[1],nodeColorRGB[2])

                if nodeColorHSV[2] > 0.7 and nodeColorHSV[1] < 0.4:
                    textColor = '#262626'

            width = 115
            height = 60


            if (len(set([i.Class() for i in selectedNodes]))) > 1:
                name = 'Selection'

        else:

            name = open(name + '/_name.json').read()
            nodeColor = getSelectionColor()

            width = 105
            height = 35

        self.setText(name)

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        #resize font based on length of name
        fontSize = max(5,(13-(max(0,(len(name) - 11))/2)))
        font = QtGui.QFont(preferencesNode.knob('UIFont').value(), fontSize)
        self.setFont(font)

        self.setStyleSheet("""
                border: 1px solid black;
                color:%s;
                background:%s""" %(textColor, nodeColor))

        self.setSelectionStatus(True)

    def setSelectionStatus(self, selected = False):
        '''
        Define the style of the button for different states
        '''
        if not self.node:
            self.selected = selected

    def enterEvent(self, event):
        '''
        Change color of the button when the mouse starts hovering over it
        '''
        if not self.node:
            self.setSelectionStatus(True)
        return True

    def leaveEvent(self,event):
        if not self.node:
            self.setSelectionStatus()
        return True

    def mouseReleaseEvent(self,event):
        '''

        '''
        if not self.node:
            showHotbox(True, resetPosition = False)
        return True

#----------------------------------------------------------------------------------------------------------
#Buttons
#----------------------------------------------------------------------------------------------------------

class hotboxButton(QtWidgets.QLabel):
    '''
    Button class
    '''

    def __init__(self, name, function = None):

        super(hotboxButton, self).__init__()

        self.menuButton = False
        self.filePath = name
        self.bgColor = '#525252'

        self.borderColor = '#000000'

        #set the border color to grey for buttons from an additional repository
        for index,i in enumerate(extraRepositories):
            if name.startswith(i[1]):
                self.borderColor = '#959595'
                break

        if function != None:
            self.function = function

        else:

            #----------------------------------------------------------------------------------------------
            #Button linked to folder
            #----------------------------------------------------------------------------------------------

            if os.path.isdir(self.filePath):
                self.menuButton = True
                name = open(self.filePath+'/_name.json').read()
                self.function = 'showHotboxSubMenu("%s","%s")'%(self.filePath,name)
                self.bgColor = '#333333'

            #----------------------------------------------------------------------------------------------
            #Button linked to file
            #----------------------------------------------------------------------------------------------

            else:

                self.openFile = open(name).readlines()

                header = []
                for index, line in enumerate(self.openFile):

                    if not line.startswith('#'):
                        self.function = ''.join(self.openFile[index:])
                        break

                    header.append(line)

                tags = ['# %s: '%tag for tag in ['NAME','TEXTCOLOR','COLOR']]

                tagResults = []

                for tag in tags:
                    tagResult = None
                    for line in header:

                        if line.startswith(tag):

                            tagResult = line.split(tag)[-1].replace('\n','')
                            break

                    tagResults.append(tagResult)

                name, textColor, color = tagResults

                if textColor and name:
                    name = '<font color = "%s">%s</font>'%(textColor,name)

                if color:
                    self.bgColor = color

            #----------------------------------------------------------------------------------------------

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(105)
        self.setFixedHeight(35)

        fontSize = preferencesNode.knob('hotboxFontSize').value()
        font = QtGui.QFont(preferencesNode.knob('UIFont').value(), fontSize, QtGui.QFont.Bold)

        self.setFont(font)
        self.setWordWrap(True)
        self.setTextFormat(QtCore.Qt.RichText)

        self.setText(name)

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.selected = False
        self.setSelectionStatus()

    def invokeButton(self):
        '''
        Execute script attached to button
        '''
        with nuke.toNode(hotboxInstance.groupRoot):
            try:
                exec self.function
            except:
                self.printError(traceback.format_exc())

        #if 'close on click' is ticked, close the hotbox
        if not self.menuButton:
            if preferencesNode.knob('hotboxCloseOnClick').value() and preferencesNode.knob('hotboxTriggerDropdown').getValue():
                hotboxInstance.closeHotbox()

    def printError(self, error):

        fullError = error.splitlines()

        lineNumber = 'error determining line'

        for index, line in enumerate(reversed(fullError)):
            if line.startswith('  File "<'):

                for i in line.split(','):
                    if i.startswith(' line '):
                        lineNumber = i

                index = len(fullError)-index
                break

        fullError = fullError[index:]

        errorDescription = '\n'.join(fullError)

        scriptFolder = os.path.dirname(self.filePath)
        scriptFolderName = os.path.basename(scriptFolder)

        buttonName = [self.text()]

        while len(scriptFolderName) == 3 and scriptFolderName.isdigit():

            name = open(scriptFolder+'/_name.json').read()
            buttonName.insert(0, name)
            scriptFolder = os.path.dirname(scriptFolder)
            scriptFolderName = os.path.basename(scriptFolder)

        for i in range(2):
            buttonName.insert(0, os.path.basename(scriptFolder))
            scriptFolder = os.path.dirname(scriptFolder)

        hotboxError = '\nW_HOTBOX ERROR: %s -%s:\n\n%s'%('/'.join(buttonName),lineNumber,errorDescription)

        #print error
        print hotboxError
        nuke.tprint(hotboxError)

    def setSelectionStatus(self, selected = False):
        '''
        Define the style of the button for different states
        '''

        #if button becomes selected
        if selected:
            self.setStyleSheet("""
                                border: 1px solid black;
                                background:%s;
                                color:#eeeeee;
                                """%getSelectionColor())

        #if button becomes unselected
        else:
            self.setStyleSheet("""
                                border: 1px solid %s;
                                background:%s;
                                color:#eeeeee;
                                """%(self.borderColor, self.bgColor))


        if preferencesNode.knob('hotboxExecuteOnClose').value():

            global hotboxInstance
            if hotboxInstance != None:

                hotboxInstance.activeButton = None

                #if launch mode set to Press and Hold and the button is a menu button,
                #dont open a submenu upon shortcut release

                if not self.menuButton and not preferencesNode.knob('hotboxTriggerDropdown').getValue():
                    if selected:
                        hotboxInstance.activeButton = self

        self.selected = selected

    def enterEvent(self, event):
        '''
        Change color of the button when the mouse starts hovering over it
        '''
        self.setSelectionStatus(True)
        return True

    def leaveEvent(self,event):
        '''
        Change color of the button when the mouse stops hovering over it
        '''
        self.setSelectionStatus()
        return True

    def mouseReleaseEvent(self,event):
        '''
        Execute the buttons' self.function (str)
        '''
        if self.selected:
            nuke.Undo().name(self.text())
            nuke.Undo().begin()

            self.invokeButton()
            nuke.Undo().end()

        return True

#----------------------------------------------------------------------------------------------------------
# Preferences
#----------------------------------------------------------------------------------------------------------

def addToPreferences(knobObject, tooltip = None):
    '''
    Add a knob to the preference panel.
    Save current preferences to the prefencesfile in the .nuke folder.
    '''

    if knobObject.name() not in preferencesNode.knobs().keys():

        if tooltip != None:
            knobObject.setTooltip(tooltip)

        preferencesNode.addKnob(knobObject)
        savePreferencesToFile()
        return preferencesNode.knob(knobObject.name())

def savePreferencesToFile():
    '''
    Save current preferences to the prefencesfile in the .nuke folder.
    Pythonic alternative to the 'ok' button of the preferences panel.
    '''

    nukeFolder = os.path.expanduser('~') + '/.nuke/'
    preferencesFile = nukeFolder + 'preferences%i.%i.nk' %(nuke.NUKE_VERSION_MAJOR,nuke.NUKE_VERSION_MINOR)

    preferencesNode = nuke.toNode('preferences')

    customPrefences = preferencesNode.writeKnobs( nuke.WRITE_USER_KNOB_DEFS | nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT | nuke.TO_VALUE )
    customPrefences = customPrefences.replace('\n','\n  ')

    preferencesCode = 'Preferences {\n inputs 0\n name Preferences%s\n}' %customPrefences

    # write to file
    openPreferencesFile = open( preferencesFile , 'w' )
    openPreferencesFile.write( preferencesCode )
    openPreferencesFile.close()

def deletePreferences():
    '''
    Delete all the W_hotbox related items in the properties panel.
    '''

    firstLaunch = True
    for i in preferencesNode.knobs().keys():
        if 'hotbox' in i:
            preferencesNode.removeKnob(preferencesNode.knob(i))
            firstLaunch = False

    #remove TabKnob
    try:
        preferencesNode.removeKnob(preferencesNode.knob('hotboxLabel'))
    except:
        pass

    if not firstLaunch:
        savePreferencesToFile()

def addPreferences():
    '''
    Add knobs to the preferences needed for this module to work properly.
    '''
    
    homeFolder = os.getenv('HOME').replace('\\','/') + '/.nuke'
    
    addToPreferences(nuke.Tab_Knob('hotboxLabel','W_hotbox'))
    addToPreferences(nuke.Text_Knob('hotboxGeneralLabel','<b>General</b>'))

    #version knob to check whether the hotbox was updated
    versionKnob = nuke.String_Knob('hotboxVersion','version')
    versionKnob.setValue(version)
    addToPreferences(versionKnob)
    preferencesNode.knob('hotboxVersion').setVisible(False)

    #location knob
    locationKnob = nuke.File_Knob('hotboxLocation','Hotbox location')

    tooltip = "The folder on disk the Hotbox uses to store the Hotbox buttons. Make sure this path links to the folder containing the 'All','Single' and 'Multiple' folders."

    locationKnobAdded = addToPreferences(locationKnob, tooltip)

    if locationKnobAdded != None:
        locationKnob.setValue(homeFolder + '/W_hotbox')

    #icons knob
    iconLocationKnob = nuke.File_Knob('hotboxIconLocation','Icons location')
    iconLocationKnob.setValue(homeFolder +'/icons/W_hotbox')

    tooltip = "The folder on disk the where the Hotbox related icons are stored. Make sure this path links to the folder containing the PNG files."
    addToPreferences(iconLocationKnob, tooltip)

    #open manager button
    openManagerKnob = nuke.PyScript_Knob('hotboxOpenManager','open hotbox manager','W_hotboxManager.showHotboxManager()')
    openManagerKnob.setFlag(nuke.STARTLINE)

    tooltip = "Open the Hotbox Manager."

    addToPreferences(openManagerKnob, tooltip)

    #open in file system button knob
    openFolderKnob = nuke.PyScript_Knob('hotboxOpenFolder','open hotbox folder','W_hotbox.revealInBrowser(True)')

    tooltip = "Open the folder containing the files that store the Hotbox buttons. It's advised not to mess around in this folder unless you understand what you're doing."

    addToPreferences(openFolderKnob, tooltip)

    #delete preferences button knob
    deletePreferencesKnob = nuke.PyScript_Knob('hotboxDeletePreferences','delete preferences','W_hotbox.deletePreferences()')

    tooltip = "Delete all the Hotbox related knobs from the Preferences Panel. After clicking this button the Preferences Panel should be closed by clicking the 'cancel' button."

    addToPreferences(deletePreferencesKnob, tooltip)

    #Launch Label knob
    addToPreferences(nuke.Text_Knob('hotboxLaunchLabel','<b>Launch</b>'))

    #shortcut knob
    shortcutKnob = nuke.String_Knob('hotboxShortcut','Shortcut')
    shortcutKnob.setValue('`')

    tooltip = "The key that triggers the Hotbox. Should be set to a single key without any modifier keys. Spacebar can be defined as 'space'. Nuke needs be restarted in order for the changes to take effect."

    addToPreferences(shortcutKnob, tooltip)
    global shortcut
    shortcut = preferencesNode.knob('hotboxShortcut').value()

    #trigger mode knob
    triggerDropdownKnob = nuke.Enumeration_Knob('hotboxTriggerDropdown', 'Launch mode',['Press and Hold','Single Tap'])

    tooltip = "The way the hotbox is launched. When set to 'Press and Hold' the Hotbox will appear whenever the shortcut is pressed and disappear as soon as the user releases the key. When set to 'Single Tap' the shortcut will toggle the Hotbox on and off."

    addToPreferences(triggerDropdownKnob, tooltip)

    #close on click
    closeAfterClickKnob = nuke.Boolean_Knob('hotboxCloseOnClick','Close on button click')
    closeAfterClickKnob.setValue(False)
    closeAfterClickKnob.clearFlag(nuke.STARTLINE)

    tooltip = "Close the Hotbox whenever a button is clicked (excluding submenus obviously). This option will only take effect when the launch mode is set to 'Single Tap'."

    addToPreferences(closeAfterClickKnob, tooltip)

    #execute on close
    executeWithoutClickKnob = nuke.Boolean_Knob('hotboxExecuteOnClose','Execute button without click')
    executeWithoutClickKnob.setValue(False)
    executeWithoutClickKnob.clearFlag(nuke.STARTLINE)

    tooltip = "Execute the button underneath the cursor whenever the Hotbox is closed."

    addToPreferences(executeWithoutClickKnob, tooltip)

    #Appearence knob
    addToPreferences(nuke.Text_Knob('hotboxAppearanceLabel','<b>Appearance</b>'))

    #color dropdown knob
    colorDropdownKnob = nuke.Enumeration_Knob('hotboxColorDropdown', 'Color scheme',['Maya','Nuke','Custom'])

    tooltip = "The color of the buttons when selected.\n\n<b>Maya</b> Autodesk Maya's muted blue.\n<b>Nuke</b> Nuke's bright orange.\n<b>Custom</b> which lets the user pick a color."

    addToPreferences(colorDropdownKnob, tooltip)

    #custom color knob
    colorCustomKnob = nuke.ColorChip_Knob('hotboxColorCustom','')
    colorCustomKnob.clearFlag(nuke.STARTLINE)

    tooltip = "The color of the buttons when selected, when the color dropdown is set to 'Custom'."

    addToPreferences(colorCustomKnob, tooltip)

    #hotbox center knob
    colorHotboxCenterKnob = nuke.Boolean_Knob('hotboxColorCenter','Colorize hotbox center')
    colorHotboxCenterKnob.setValue(True)
    colorHotboxCenterKnob.clearFlag(nuke.STARTLINE)

    tooltip = "Color the center button of the hotbox depending on the current selection. When unticked the center button will be colored a lighter tone of grey."

    addToPreferences(colorHotboxCenterKnob, tooltip)

    #auto color text
    autoTextColorKnob = nuke.Boolean_Knob('hotboxAutoTextColor','Auto adjust text color')
    autoTextColorKnob.setValue(True)
    autoTextColorKnob.clearFlag(nuke.STARTLINE)

    tooltip = "Automatically adjust the color of a button's text to its background color in order to keep enough of a difference to remain readable."

    addToPreferences(autoTextColorKnob, tooltip)

    #fontsize knob
    fontSizeKnob = nuke.Int_Knob('hotboxFontSize','Font size')
    fontSizeKnob.setValue(9)

    tooltip = "The font size of the text that appears in the hotbox buttons, unless defined differently on a per-button level."

    addToPreferences(fontSizeKnob, tooltip)

    #fontsize manager's script editor knob
    fontSizeScriptEditorKnob = nuke.Int_Knob('hotboxScriptEditorFontSize','Font size script editor')
    fontSizeScriptEditorKnob.setValue(11)
    fontSizeScriptEditorKnob.clearFlag(nuke.STARTLINE)

    tooltip = "The font size of the text that appears in the hotbox manager's script editor."

    addToPreferences(fontSizeScriptEditorKnob, tooltip)

    addToPreferences(nuke.Text_Knob('hotboxItemsLabel','<b>Items per Row</b>'))

    #row amount selection knob
    rowAmountSelectionKnob = nuke.Int_Knob('hotboxRowAmountSelection', 'Selection specific')
    rowAmountSelectionKnob.setValue(3)

    tooltip = "The maximum amount of buttons a row in the upper half of the Hotbox can contain. When the row's maximum capacity is reached a new row will be started. This new row's maximum capacity will be incremented by the step size."

    addToPreferences(rowAmountSelectionKnob, tooltip)

    #row amount all knob
    rowAmountSelectionAll = nuke.Int_Knob('hotboxRowAmountAll','All')
    rowAmountSelectionAll.setValue(3)

    tooltip = "The maximum amount of buttons a row in the lower half of the Hotbox can contain. When the row's maximum capacity is reached a new row will be started.This new row's maximum capacity will be incremented by the step size."

    addToPreferences(rowAmountSelectionAll, tooltip)

    #stepsize knob
    stepSizeKnob = nuke.Int_Knob('hotboxRowStepSize','Step size')
    stepSizeKnob.setValue(1)

    tooltip = "The amount a buttons every new row's maximum capacity will be increased by. Having a number unequal to zero will result in a triangular shape when having multiple rows of buttons."

    addToPreferences(stepSizeKnob, tooltip)

    #spawnmode knob
    spawnModeKnob = nuke.Boolean_Knob('hotboxButtonSpawnMode','Add new buttons to the sides')
    spawnModeKnob.setValue(True)
    spawnModeKnob.setFlag(nuke.STARTLINE)

    tooltip = "Add new buttons left and right of the row alternately, instead of to the right, in order to preserve muscle memory."

    addToPreferences(spawnModeKnob, tooltip)

    #hide the iconLocation knob if environment varible called 'W_HOTBOX_HIDE_ICON_LOC' is set to 'true' or '1'
    preferencesNode.knob('hotboxIconLocation').setVisible(True)
    if 'W_HOTBOX_HIDE_ICON_LOC' in os.environ.keys():
        if os.environ['W_HOTBOX_HIDE_ICON_LOC'].lower() in ['true','1']:
            preferencesNode.knob('hotboxIconLocation').setVisible(False)

    savePreferencesToFile()

def updatePreferences():
    '''
    Check whether the hotbox was updated since the last launch. If so refresh the preferences.
    '''


    allKnobs = preferencesNode.knobs().keys()

    #Older versions of the hotbox had a knob called 'iconLocation'.
    #This was a mistake and the knob was supposed to be called
    #'hotboxIconLocation', similar to the rest of the knobs.

    forceUpdate = False

    if 'iconLocation' in allKnobs and 'hotboxIconLocation' not in allKnobs:

        currentSetting = preferencesNode.knob('iconLocation').value()

        #delete 'iconLocation'
        preferencesNode.removeKnob(preferencesNode.knob('iconLocation'))

        #re-add 'hotboxIconLocation'
        iconLocationKnob = nuke.File_Knob('hotboxIconLocation','Icons location')
        iconLocationKnob.setValue(currentSetting)
        addToPreferences(iconLocationKnob)

        forceUpdate = True

    allKnobs = preferencesNode.knobs().keys()
    proceedUpdate = True

    if 'hotboxVersion' in allKnobs or forceUpdate:

        if not forceUpdate:
            try:
                if float(version) == float(preferencesNode.knob('hotboxVersion').value()):
                    proceedUpdate = False
            except:
                proceedUpdate = True

        if proceedUpdate:
            currentSettings = {knob:preferencesNode.knob(knob).value() for knob in allKnobs if knob.startswith('hotbox') and knob != 'hotboxVersion'}

            #delete all the preferences
            deletePreferences()

            #re-add all the knobs
            addPreferences()

            #Restore
            for knob in currentSettings.keys():
                try:
                    preferencesNode.knob(knob).setValue(currentSettings[knob])
                except:
                    pass

            #save to file
            savePreferencesToFile()

#----------------------------------------------------------------------------------------------------------
#Color
#----------------------------------------------------------------------------------------------------------

def interface2rgb(hexValue, normalize = True):
    '''
    Convert a color stored as a 32 bit value as used by nuke for interface colors to normalized rgb values.

    '''
    return [(0xFF & hexValue >>  i) / 255.0 for i in [24,16,8]]


def rgb2hex(rgbaValues):
    '''
    Convert a color stored as normalized rgb values to a hex.
    '''
    if len(rgbaValues) < 3:
        return
    return '#%02x%02x%02x' % (rgbaValues[0]*255,rgbaValues[1]*255,rgbaValues[2]*255)

def hex2rgb(hexColor):
    '''
    Convert a color stored as hex to rgb values.
    '''
    hexColor = hexColor.lstrip('#')
    return tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))

def rgb2interface(rgb):
    '''
    Convert a color stored as rgb values to a 32 bit value as used by nuke for interface colors.
    '''
    if len(rgb) == 3:
        rgb = rgb + (255,)

    return int('%02x%02x%02x%02x'%rgb,16)

def getTileColor(node = None):
    '''
    If a node has it's color set automatically, the 'tile_color' knob will return 0.
    If so, this function will scan through the preferences to find the correct color value.
    '''

    if not node:
        node = nuke.selectedNode()

    interfaceColor = node.knob('tile_color').value()

    if interfaceColor == 0:
        interfaceColor = nuke.defaultNodeColor(node.Class())

    return interfaceColor

def getSelectionColor():
    '''
    Return color to be used for the selected items of the hotbox.
    '''

    customColor = rgb2hex(interface2rgb(preferencesNode.knob('hotboxColorCustom').value()))
    colorMode = int(preferencesNode.knob('hotboxColorDropdown').getValue())
    
    return['#5285a6','#f7931e',customColor][colorMode]

#----------------------------------------------------------------------------------------------------------

def revealInBrowser(startFolder = False):
    '''
    Reveal the hotbox folder in a filebrowser
    '''
    if startFolder:
        path = preferencesNode.knob('hotboxLocation').value()

    else:
        try:
            path =  hotboxInstance.topLayout.folderList[0]
        except:
            path = hotboxInstance.topLayout.path + hotboxInstance.mode

    if not os.path.exists(path):
        path = os.path.dirname(path)

    if operatingSystem == "Windows":
        os.startfile(path)
    elif operatingSystem == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def getFileBrowser():
    '''
    Determine the name of the file browser on the current system.
    '''

    if operatingSystem == "Windows":
        fileBrowser = 'Explorer'
    elif operatingSystem == "Darwin":
        fileBrowser = 'Finder'
    else:
        fileBrowser = 'file browser'

    return fileBrowser

#----------------------------------------------------------------------------------------------------------

def showHotbox(force = False, resetPosition = True):

    global hotboxInstance

    #is launch mode is set to single tap, close the hotbox if it's open
    if preferencesNode.knob('hotboxTriggerDropdown').getValue() and not force:
        if hotboxInstance != None and hotboxInstance.active:
            hotboxInstance.closeHotbox(hotkey = True)
            return

    if force:
        hotboxInstance.active = False
        hotboxInstance.close()

    if resetPosition:
        global lastPosition
        lastPosition = ''

    if hotboxInstance == None or not hotboxInstance.active:
        hotboxInstance = hotbox(position = lastPosition)
        hotboxInstance.show()

def showHotboxSubMenu(path, name):
    global hotboxInstance
    hotboxInstance.active = False
    if hotboxInstance == None or not hotboxInstance.active:
        hotboxInstance = hotbox(True, path, name)
        hotboxInstance.show()

def showHotboxManager():
    '''
    Open the hotbox manager from the hotbox
    '''
    hotboxInstance.closeHotbox()
    W_hotboxManager.showHotboxManager()

#----------------------------------------------------------------------------------------------------------


#add knobs to preferences
preferencesNode = nuke.toNode('preferences')
updatePreferences()
addPreferences()

#----------------------------------------------------------------------------------------------------------

#make sure the archive folders are present, if not, create them

hotboxLocationPath = preferencesNode.knob('hotboxLocation').value().replace('\\','/')
if hotboxLocationPath[-1] != '/':
    hotboxLocationPath += '/'

for subFolder in ['','Single','Multiple','All','Single/No Selection','Templates']:
    subFolderPath = hotboxLocationPath + subFolder
    if not os.path.isdir(subFolderPath):
        try:
            os.mkdir(subFolderPath)
        except:
            pass

#----------------------------------------------------------------------------------------------------------
# MENU ITEMS
#----------------------------------------------------------------------------------------------------------

menubar = nuke.menu('Nuke')

menubar.addCommand('Edit/-', '', '')
menubar.addCommand('Edit/W_hotbox/Open W_hotbox',showHotbox, shortcut)
menubar.addCommand('Edit/W_hotbox/-', '', '')
menubar.addCommand('Edit/W_hotbox/Open Hotbox Manager', 'W_hotboxManager.showHotboxManager()')
menubar.addCommand('Edit/W_hotbox/Open in %s'%getFileBrowser(), revealInBrowser)
menubar.addCommand('Edit/W_hotbox/-', '', '')
menubar.addCommand('Edit/W_hotbox/Repair', 'W_hotboxManager.repairHotbox()')
menubar.addCommand('Edit/W_hotbox/Clear/Clear Everything', 'W_hotboxManager.clearHotboxManager()')
menubar.addCommand('Edit/W_hotbox/Clear/Clear Section/Single', 'W_hotboxManager.clearHotboxManager(["Single"])')
menubar.addCommand('Edit/W_hotbox/Clear/Clear Section/Multiple', 'W_hotboxManager.clearHotboxManager(["Multiple"])')
menubar.addCommand('Edit/W_hotbox/Clear/Clear Section/All', 'W_hotboxManager.clearHotboxManager(["All"])')
menubar.addCommand('Edit/W_hotbox/Clear/Clear Section/-', '', '')
menubar.addCommand('Edit/W_hotbox/Clear/Clear Section/Templates', 'W_hotboxManager.clearHotboxManager(["Templates"])')

#----------------------------------------------------------------------------------------------------------
# EXTRA REPOSTITORIES
#----------------------------------------------------------------------------------------------------------
'''
Add them like this:

W_HOTBOX_REPO_PATHS=/path1:/path2:/path3
W_HOTBOX_REPO_NAMES=name1:name2:name3

'''

extraRepositories = []

if 'W_HOTBOX_REPO_PATHS' in os.environ and 'W_HOTBOX_REPO_NAMES' in os.environ.keys():

    extraRepositoriesPaths = os.environ['W_HOTBOX_REPO_PATHS'].split(os.pathsep)
    extraRepositoriesNames = os.environ['W_HOTBOX_REPO_NAMES'].split(os.pathsep)

    for index, i in enumerate(range(min(len(extraRepositoriesPaths),len(extraRepositoriesNames)))):
        path = extraRepositoriesPaths[index].replace('\\','/')

        #make sure last character is a '/'
        if path[-1] != '/':
            path += '/'

        name = extraRepositoriesNames[index]
        if name not in [i[0] for i in extraRepositories] and path not in [i[1] for i in extraRepositories]:
            extraRepositories.append([name,path])



    if len(extraRepositories) > 0:
        menubar.addCommand('Edit/W_hotbox/-', '', '')
        for i in extraRepositories:
            menubar.addCommand('Edit/W_hotbox/Special/Open Hotbox Manager - %s'%i[0], 'W_hotboxManager.showHotboxManager(path="%s")'%i[1])

#----------------------------------------------------------------------------------------------------------

hotboxInstance = None
lastPosition = ''

#----------------------------------------------------------------------------------------------------------

nuke.tprint('W_hotbox v%s, built %s.\nCopyright (c) 2016 Wouter Gilsing. All Rights Reserved.'%(version,releaseDate))
