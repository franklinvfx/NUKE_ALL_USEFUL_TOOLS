#-------------------------------------------------
# Knob Scripter by Adrian Pueyo
# Script editor for python and callback knobs
# adrianpueyo.com, 2017-2018
version = "1.2"
#-------------------------------------------------

import nuke
import os
import json
from nukescripts import panels
import sys
import nuke

if nuke.NUKE_VERSION_MAJOR < 11: # < nuke11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
else: # > nuke11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets

class KnobScripter(QtGuiWidgets.QWidget):

    def __init__(self,node=nuke.root(),knob="knobChanged"):

        super(KnobScripter,self).__init__()
        self.node = node
        self.knob = knob
        self.unsavedKnobs = {}
        self.fontSize = 11
        self.windowDefaultSize = [500, 300]

        # Load prefs
        self.prefs_txt = os.path.expandvars(os.path.expanduser("~/.nuke/KnobScripter_prefs.txt"))
        self.loadedPrefs = self.loadPrefs()
        if self.loadedPrefs != []:
            try:
                self.fontSize = self.loadedPrefs['font_size']
                self.windowDefaultSize = [self.loadedPrefs['window_default_w'], self.loadedPrefs['window_default_h']]
            except TypeError:
                print("KnobScripter: Failed to load preferences.")

        # KnobScripter Panel
        self.resize(self.windowDefaultSize[0],self.windowDefaultSize[1])
        self.setWindowTitle("KnobScripter - %s %s" % (self.node.name(),self.knob))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.move(QtGui.QCursor().pos() - QtCore.QPoint(32,74))

        # Node/Knob Selection menu
        self.current_node_label = QtGuiWidgets.QLabel("Node: <b> %s </b>"%self.node.name())
        self.current_node_change_button = QtGuiWidgets.QPushButton("Change")
        self.current_node_change_button.setToolTip("Change node to selected")
        self.current_node_change_button.clicked.connect(self.changeNode)
        self.current_knob_label = QtGuiWidgets.QLabel("Knob: ")
        self.current_knob_dropdown = QtGuiWidgets.QComboBox()
        self.updateKnobDropdown()
        self.current_knob_dropdown.currentIndexChanged.connect(lambda: self.loadKnobValue(False,updateDict=True))
        self.current_knob_prefs_button = QtGuiWidgets.QPushButton("Preferences")
        self.current_knob_prefs_button.clicked.connect(self.openPrefs)

        # Script Editor (adapted from Wouter Gilsing's, read class definition below)
        self.scriptEditorScript = KnobScripterEditorWidget(self)
        self.scriptEditorScript.setMinimumHeight(100)
        self.scriptEditorScript.setStyleSheet('background:#282828;color:#EEE;') # Main Colors
        KSScriptEditorHighlighter(self.scriptEditorScript.document())
        self.scriptEditorFont = QtGui.QFont()
        self.scriptEditorFont.setFamily("Courier")
        self.scriptEditorFont.setStyleHint(QtGui.QFont.Monospace)
        self.scriptEditorFont.setFixedPitch(True)
        self.scriptEditorFont.setPointSize(self.fontSize)
        self.scriptEditorScript.setFont(self.scriptEditorFont)
        self.scriptEditorScript.setTabStopWidth(4 * QtGui.QFontMetrics(self.scriptEditorFont).width(' '))

        # Lower Buttons
        self.get_btn = QtGuiWidgets.QPushButton("Reload")
        self.get_all_btn = QtGuiWidgets.QPushButton("Reload All")
        self.arrows_label = QtGuiWidgets.QLabel("&raquo;")
        self.arrows_label.setTextFormat(QtCore.Qt.RichText)
        self.arrows_label.setStyleSheet('color:#BBB')
        self.set_btn = QtGuiWidgets.QPushButton("Save")
        self.set_all_btn = QtGuiWidgets.QPushButton("Save All")
        self.close_btn = QtGuiWidgets.QPushButton("Close")
        self.get_btn.clicked.connect(self.loadKnobValue)
        self.get_all_btn.clicked.connect(self.loadAllKnobValues)
        self.set_btn.clicked.connect(lambda: self.saveKnobValue(False))
        self.set_all_btn.clicked.connect(self.saveAllKnobValues)
        self.close_btn.clicked.connect(self.close)

        # Layouts
        master_layout = QtGuiWidgets.QVBoxLayout()
        nodeknob_layout = QtGuiWidgets.QHBoxLayout()
        nodeknob_layout.addWidget(self.current_node_label)
        nodeknob_layout.addWidget(self.current_node_change_button)
        nodeknob_layout.addSpacing(10)
        nodeknob_layout.addWidget(self.current_knob_label)
        nodeknob_layout.addWidget(self.current_knob_dropdown)
        nodeknob_layout.addSpacing(10)
        nodeknob_layout.addStretch()
        nodeknob_layout.addWidget(self.current_knob_prefs_button)
        self.btn_layout = QtGuiWidgets.QHBoxLayout()
        self.btn_layout.addWidget(self.get_btn)
        self.btn_layout.addWidget(self.get_all_btn)
        self.btn_layout.addWidget(self.arrows_label)
        self.btn_layout.addWidget(self.set_btn)
        self.btn_layout.addWidget(self.set_all_btn)
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.close_btn)
        master_layout.addLayout(nodeknob_layout)
        master_layout.addWidget(self.scriptEditorScript)
        master_layout.addLayout(self.btn_layout)
        self.setLayout(master_layout)

        # Set default values
        self.setCurrentKnob(self.knob)
        self.loadKnobValue(check = False)
        self.scriptEditorScript.setFocus()

    # Populate knob dropdown list
    def updateKnobDropdown(self):
        self.current_knob_dropdown.clear() # First remove all items
        defaultKnobs = ["knobChanged", "onCreate", "onScriptLoad", "onScriptSave", "onScriptClose", "onDestroy",
                        "updateUI", "autolabel", "beforeRender", "beforeFrameRender", "afterFrameRender", "afterRender"]
        permittedKnobClasses = ["PyScript_Knob", "PythonCustomKnob"]
        counter = 0
        for i in self.node.knobs():
            if i not in defaultKnobs and self.node.knob(i).Class() in permittedKnobClasses:
                self.current_knob_dropdown.addItem(i)
                counter += 1
        if counter > 0:
            self.current_knob_dropdown.insertSeparator(counter)
            counter += 1
            self.current_knob_dropdown.insertSeparator(counter)
            counter += 1
        for i in self.node.knobs():
            if i in defaultKnobs:
                self.current_knob_dropdown.addItem(i)
                counter += 1

    # Set current knob
    def setCurrentKnob(self, knobToSet):
        KnobDropdownItems = [self.current_knob_dropdown.itemText(i) for i in range(self.current_knob_dropdown.count())]
        if knobToSet in KnobDropdownItems:
            knobIndex = self.current_knob_dropdown.findText(knobToSet, QtCore.Qt.MatchFixedString)
            if knobIndex >= 0:
                self.current_knob_dropdown.setCurrentIndex(knobIndex)

    # Clear unchanged knobs from the dict and return the number of unsaved knobs
    def updateUnsavedKnobs(self):
        edited_knobValue = self.scriptEditorScript.toPlainText()
        self.unsavedKnobs[self.knob] = edited_knobValue
        if len(self.unsavedKnobs) > 0:
            for k in self.unsavedKnobs.copy():
                if self.node.knob(k):
                    if str(self.node.knob(k).value()) == str(self.unsavedKnobs[k]):
                        del self.unsavedKnobs[k]
                else:
                    del self.unsavedKnobs[k]
        return len(self.unsavedKnobs)

    # Change node
    def changeNode(self, newNode=""):
        selection = nuke.selectedNodes()
        updatedCount = self.updateUnsavedKnobs()
        if not len(selection):
            nuke.message("Please select one or more nodes!")
        else:
            # If already selected, pass
            if selection[0].name() == self.node.name():
                return
            elif updatedCount > 0:
                msgBox = QtGuiWidgets.QMessageBox()
                msgBox.setText(
                    "Save changes to %s knob%s before changing the node?" % (str(updatedCount), int(updatedCount > 1) * "s"))
                msgBox.setStandardButtons(QtGuiWidgets.QMessageBox.Yes | QtGuiWidgets.QMessageBox.No | QtGuiWidgets.QMessageBox.Cancel)
                msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                msgBox.setDefaultButton(QtGuiWidgets.QMessageBox.Yes)
                reply = msgBox.exec_()
                if reply == QtGuiWidgets.QMessageBox.Yes:
                    self.saveAllKnobValues(check=False)
                    print self.unsavedKnobs
                elif reply == QtGuiWidgets.QMessageBox.Cancel:
                    return
            if len(selection) > 1:
                msgBox = QtGuiWidgets.QMessageBox()
                msgBox.setText("More than one node selected.\nChanging knobChanged editor to %s" % selection[0].name())
                msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                msgBox.exec_()
            # Reinitialise everything, wooo!
            self.node = selection[0]
            self.scriptEditorScript.setPlainText("")
            self.unsavedKnobs = {}
            self.setWindowTitle("KnobScripter - %s %s" % (self.node.name(), self.knob))
            self.current_node_label.setText("Node: <b> %s </b>" % self.node.name())
            self.updateKnobDropdown()
            self.loadKnobValue(False)
            self.scriptEditorScript.setFocus()
        return

    # Open the preferences panel
    def openPrefs(self):
        global ks_prefs
        ks_prefs = KnobScripterPrefs(self)
        ks_prefs.show()

    # Load prefs
    def loadPrefs(self):
        if not os.path.isfile(self.prefs_txt):
            return []
        else:
            with open(self.prefs_txt, "r") as f:
                prefs = json.load(f)
                return prefs

    # Get the content of the knob knobChanged and populate the editor
    def loadKnobValue(self, check=True, updateDict=False):
        dropdown_value = self.current_knob_dropdown.currentText()
        try:
            obtained_knobValue = str(self.node[dropdown_value].value())
            edited_knobValue = self.scriptEditorScript.toPlainText()
        except:
            error_message = QtGuiWidgets.QMessageBox.information(None, "", "Unable to find %s.%s"%(self.node.name(),dropdown_value))
            error_message.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            error_message.exec_()
            return
        # If there were changes to the previous knob, update the dictionary
        if updateDict==True:
            self.unsavedKnobs[self.knob] = edited_knobValue
        prev_knob = self.knob
        self.knob = self.current_knob_dropdown.currentText()
        if check and obtained_knobValue != edited_knobValue:
            msgBox = QtGuiWidgets.QMessageBox()
            msgBox.setText("The Script Editor has been modified.")
            msgBox.setInformativeText("Do you want to overwrite the current code on this editor?")
            msgBox.setStandardButtons(QtGuiWidgets.QMessageBox.Yes | QtGuiWidgets.QMessageBox.No)
            msgBox.setIcon(QtGuiWidgets.QMessageBox.Question)
            msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msgBox.setDefaultButton(QtGuiWidgets.QMessageBox.Yes)
            reply = msgBox.exec_()
            if reply == QtGuiWidgets.QMessageBox.No:
                self.setCurrentKnob(prev_knob)
                return
        # If order comes from a dropdown update, update value from dictionary if possible, otherwise update normally
        if updateDict:
            if self.knob in self.unsavedKnobs:
                obtained_knobValue = self.unsavedKnobs[self.knob]
        self.scriptEditorScript.setPlainText(obtained_knobValue)
        self.setWindowTitle("KnobScripter - %s %s" % (self.node.name(), self.knob))
        return

    # Save the text from the editor to the node's knobChanged knob
    def saveKnobValue(self, check=True):
        dropdown_value = self.current_knob_dropdown.currentText()
        try:
            obtained_knobValue = str(self.node[dropdown_value].value())
            self.knob = self.current_knob_dropdown.currentText()
        except:
            error_message = QtGuiWidgets.QMessageBox.information(None, "", "Unable to find %s.%s"%(self.node.name(),dropdown_value))
            error_message.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            error_message.exec_()
            return
        edited_knobValue = self.scriptEditorScript.toPlainText()
        if check and obtained_knobValue != edited_knobValue:
            msgBox = QtGuiWidgets.QMessageBox()
            msgBox.setText("Do you want to overwrite %s.%s?"%(self.node.name(),dropdown_value))
            msgBox.setStandardButtons(QtGuiWidgets.QMessageBox.Yes | QtGuiWidgets.QMessageBox.No)
            msgBox.setIcon(QtGuiWidgets.QMessageBox.Question)
            msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msgBox.setDefaultButton(QtGuiWidgets.QMessageBox.Yes)
            reply = msgBox.exec_()
            if reply == QtGuiWidgets.QMessageBox.No:
                return
        self.node[self.current_knob_dropdown.currentText()].setValue(edited_knobValue)
        if self.knob in self.unsavedKnobs:
            del self.unsavedKnobs[self.knob]
        return

    # Load all knobs button's function
    def loadAllKnobValues(self):
        if len(self.unsavedKnobs)>=1:
            msgBox = QtGuiWidgets.QMessageBox()
            msgBox.setText("Do you want to reload all python and callback knobs?")
            msgBox.setInformativeText("Unsaved changes on this editor will be lost.")
            msgBox.setStandardButtons(QtGuiWidgets.QMessageBox.Yes | QtGuiWidgets.QMessageBox.No)
            msgBox.setIcon(QtGuiWidgets.QMessageBox.Question)
            msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msgBox.setDefaultButton(QtGuiWidgets.QMessageBox.Yes)
            reply = msgBox.exec_()
            if reply == QtGuiWidgets.QMessageBox.No:
                return
        self.unsavedKnobs = {}
        return

    # Save all knobs button's function
    def saveAllKnobValues(self, check=True):
        if self.updateUnsavedKnobs() > 0 and check:
            msgBox = QtGuiWidgets.QMessageBox()
            msgBox.setText("Do you want to save all modified python and callback knobs?")
            msgBox.setStandardButtons(QtGuiWidgets.QMessageBox.Yes | QtGuiWidgets.QMessageBox.No)
            msgBox.setIcon(QtGuiWidgets.QMessageBox.Question)
            msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msgBox.setDefaultButton(QtGuiWidgets.QMessageBox.Yes)
            reply = msgBox.exec_()
            if reply == QtGuiWidgets.QMessageBox.No:
                return
        saveErrors = 0
        savedCount = 0
        for k in self.unsavedKnobs.copy():
            try:
                self.node.knob(k).setValue(self.unsavedKnobs[k])
                del self.unsavedKnobs[k]
                savedCount += 1
            except:
                saveErrors+=1
        if saveErrors > 0:
            errorBox = QtGuiWidgets.QMessageBox()
            errorBox.setText("Error saving %s knob%s." % (str(saveErrors),int(saveErrors>1)*"s"))
            errorBox.setIcon(QtGuiWidgets.QMessageBox.Warning)
            errorBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            errorBox.setDefaultButton(QtGuiWidgets.QMessageBox.Yes)
            reply = errorBox.exec_()
        else:
            print "KnobScripter: %s knobs saved" % str(savedCount)
        return

    def closeEvent(self, event):
        updatedCount = self.updateUnsavedKnobs()
        if updatedCount > 0:
            msgBox = QtGuiWidgets.QMessageBox()
            msgBox.setText("Save changes to %s knob%s before closing?" % (str(updatedCount),int(updatedCount>1)*"s"))
            msgBox.setStandardButtons(QtGuiWidgets.QMessageBox.Yes | QtGuiWidgets.QMessageBox.No | QtGuiWidgets.QMessageBox.Cancel)
            msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msgBox.setDefaultButton(QtGuiWidgets.QMessageBox.Yes)
            reply = msgBox.exec_()
            if reply == QtGuiWidgets.QMessageBox.Yes:
                self.saveAllKnobValues(check=False)
                event.accept()
                return
            elif reply == QtGuiWidgets.QMessageBox.Cancel:
                event.ignore()
                return
        else:
            event.accept()


class KnobScripterPane(KnobScripter):
    def __init__(self, node=nuke.root(), knob="knobChanged"):
        super(KnobScripterPane, self).__init__()
        self.btn_layout.removeWidget(self.close_btn)
        self.close_btn.deleteLater()
        self.close_btn = None

        ksSignature = QtGuiWidgets.QLabel(
            '<a href="http://www.adrianpueyo.com/" style="color:#888;text-decoration:none"><b>KnobScripter </b></a>v'+version)
        ksSignature.setOpenExternalLinks(True)
        ksSignature.setStyleSheet('''color:#555;font-size:9px;''')
        self.btn_layout.addWidget(ksSignature)

    def deleteCloseButton(self):
        b = self.btn_layout.takeAt(2)
        b.widget().deleteLater()



#------------------------------------------------------------------------------------------------------
# Script Editor Widget
# Wouter Gilsing built an incredibly useful python script editor for his Hotbox Manager, so I had it
# really easy for this part! I made it a bit simpler, leaving just the part non associated to his tool
# and tweaking the style a bit to be compatible with font size changing and stuff.
# I think this bit of code has the potential to get used in many nuke tools.
# All credit to him: http://www.woutergilsing.com/
# Originally used on W_Hotbox v1.5: http://www.nukepedia.com/python/ui/w_hotbox
#------------------------------------------------------------------------------------------------------

class KnobScripterEditorWidget(QtGuiWidgets.QPlainTextEdit):

    # Signal that will be emitted when the user has changed the text
    userChangedEvent = QtCore.Signal()

    def __init__(self, knobScripter):
        super(KnobScripterEditorWidget, self).__init__()
        self.knobScripter = knobScripter

        # Setup line numbers
        self.lineNumberArea = KSLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth()

        # Highlight line
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    #--------------------------------------------------------------------------------------------------
    # Line Numbers (extract from original comment by Wouter Gilsing)
    # While researching the implementation of line number, I had a look at Nuke's Blinkscript node. [..]
    # thefoundry.co.uk/products/nuke/developers/100/pythonreference/nukescripts.blinkscripteditor-pysrc.html
    # I stripped and modified the useful bits of the line number related parts of the code [..]
    # Credits to theFoundry for writing the blinkscripteditor, best example code I could wish for.
    #--------------------------------------------------------------------------------------------------

    def lineNumberAreaWidth(self):
        digits = 1
        maxNum = max(1, self.blockCount())
        while (maxNum >= 10):
            maxNum /= 10
            digits += 1

        space = 7 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):

        if (dy):
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth()

    def resizeEvent(self, event):
        QtGuiWidgets.QPlainTextEdit.resizeEvent(self, event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):

        if self.isReadOnly():
            return

        painter = QtGui.QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QtGui.QColor(36, 36, 36)) # Number bg


        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int( self.blockBoundingGeometry(block).translated(self.contentOffset()).top() )
        bottom = top + int( self.blockBoundingRect(block).height() )
        currentLine = self.document().findBlock(self.textCursor().position()).blockNumber()

        painter.setPen( self.palette().color(QtGui.QPalette.Text) )

        painterFont = QtGui.QFont()
        painterFont.setFamily("Courier")
        painterFont.setStyleHint(QtGui.QFont.Monospace)
        painterFont.setFixedPitch(True)
        painterFont.setPointSize(self.knobScripter.fontSize)
        painter.setFont(self.knobScripter.scriptEditorFont)

        while (block.isValid() and top <= event.rect().bottom()):

            textColor = QtGui.QColor(110, 110, 110) # Numbers

            if blockNumber == currentLine and self.hasFocus():
                textColor = QtGui.QColor(255, 170, 0) # Number highlighted

            painter.setPen(textColor)

            number = "%s" % str(blockNumber + 1)
            painter.drawText(-3, top, self.lineNumberArea.width(), self.fontMetrics().height(), QtCore.Qt.AlignRight, number)

            # Move to the next block
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    #--------------------------------------------------------------------------------------------------
    # Auto indent
    #--------------------------------------------------------------------------------------------------

    def keyPressEvent(self, event):
        '''
        Custom actions for specific keystrokes
        '''

        #if Tab convert to Space
        if event.key() == 16777217:
            self.indentation('indent')

        #if Shift+Tab remove indent
        elif event.key() == 16777218:

            self.indentation('unindent')

        #if BackSpace try to snap to previous indent level
        elif event.key() == 16777219:
            if not self.unindentBackspace():
                QtGuiWidgets.QPlainTextEdit.keyPressEvent(self, event)

        #if enter or return, match indent level
        elif event.key() in [16777220 ,16777221]:
            #QtGuiWidgets.QPlainTextEdit.keyPressEvent(self, event)
            self.indentNewLine()
        else:
            QtGuiWidgets.QPlainTextEdit.keyPressEvent(self, event)

    #--------------------------------------------------------------------------------------------------

    def getCursorInfo(self):

        self.cursor = self.textCursor()

        self.firstChar =  self.cursor.selectionStart()
        self.lastChar =  self.cursor.selectionEnd()

        self.noSelection = False
        if self.firstChar == self.lastChar:
            self.noSelection = True

        self.originalPosition = self.cursor.position()
        self.cursorBlockPos = self.cursor.positionInBlock()
    #--------------------------------------------------------------------------------------------------

    def unindentBackspace(self):
        '''
        #snap to previous indent level
        '''
        self.getCursorInfo()

        if not self.noSelection or self.cursorBlockPos == 0:
            return False

        #check text in front of cursor
        textInFront = self.document().findBlock(self.firstChar).text()[:self.cursorBlockPos]

        #check whether solely spaces
        if textInFront != ' '*self.cursorBlockPos:
            return False

        #snap to previous indent level
        spaces = len(textInFront)
        for space in range(spaces - ((spaces -1) /4) * 4 -1):
            self.cursor.deletePreviousChar()

    def indentNewLine(self):

        #in case selection covers multiple line, make it one line first
        self.insertPlainText('')

        self.getCursorInfo()

        #check how many spaces after cursor
        text = self.document().findBlock(self.firstChar).text()

        textInFront = text[:self.cursorBlockPos]

        if len(textInFront) == 0:
            self.insertPlainText('\n')
            return

        indentLevel = 0
        for i in textInFront:
            if i == ' ':
                indentLevel += 1
            else:
                break

        indentLevel /= 4

        #find out whether textInFront's last character was a ':'
        #if that's the case add another indent.
        #ignore any spaces at the end, however also
        #make sure textInFront is not just an indent
        if textInFront.count(' ') != len(textInFront):
            while textInFront[-1] == ' ':
                textInFront = textInFront[:-1]

        if textInFront[-1] == ':':
            indentLevel += 1

        #new line
        self.insertPlainText('\n')
        #match indent
        self.insertPlainText(' '*(4*indentLevel))

    def indentation(self, mode):

        self.getCursorInfo()

        #if nothing is selected and mode is set to indent, simply insert as many
        #space as needed to reach the next indentation level.
        if self.noSelection and mode == 'indent':

            remainingSpaces = 4 - (self.cursorBlockPos%4)
            self.insertPlainText(' '*remainingSpaces)
            return

        selectedBlocks = self.findBlocks(self.firstChar, self.lastChar)
        beforeBlocks = self.findBlocks(last = self.firstChar -1, exclude = selectedBlocks)
        afterBlocks = self.findBlocks(first = self.lastChar + 1, exclude = selectedBlocks)

        beforeBlocksText = self.blocks2list(beforeBlocks)
        selectedBlocksText = self.blocks2list(selectedBlocks, mode)
        afterBlocksText = self.blocks2list(afterBlocks)

        combinedText = '\n'.join(beforeBlocksText + selectedBlocksText + afterBlocksText)

        #make sure the line count stays the same
        originalBlockCount = len(self.toPlainText().split('\n'))
        combinedText = '\n'.join(combinedText.split('\n')[:originalBlockCount])

        self.clear()
        self.setPlainText(combinedText)

        if self.noSelection:
            self.cursor.setPosition(self.lastChar)

        #check whether the the orignal selection was from top to bottom or vice versa
        else:
            if self.originalPosition == self.firstChar:
                first = self.lastChar
                last = self.firstChar
                firstBlockSnap = QtGui.QTextCursor.EndOfBlock
                lastBlockSnap = QtGui.QTextCursor.StartOfBlock
            else:
                first = self.firstChar
                last = self.lastChar
                firstBlockSnap = QtGui.QTextCursor.StartOfBlock
                lastBlockSnap = QtGui.QTextCursor.EndOfBlock

            self.cursor.setPosition(first)
            self.cursor.movePosition(firstBlockSnap,QtGui.QTextCursor.MoveAnchor)
            self.cursor.setPosition(last,QtGui.QTextCursor.KeepAnchor)
            self.cursor.movePosition(lastBlockSnap,QtGui.QTextCursor.KeepAnchor)

        self.setTextCursor(self.cursor)

    def findBlocks(self, first = 0, last = None, exclude = []):
        blocks = []
        if last == None:
            last = self.document().characterCount()
        for pos in range(first,last+1):
            block = self.document().findBlock(pos)
            if block not in blocks and block not in exclude:
                blocks.append(block)
        return blocks

    def blocks2list(self, blocks, mode = None):
        text = []
        for block in blocks:
            blockText = block.text()
            if mode == 'unindent':
                if blockText.startswith(' '*4):
                    blockText = blockText[4:]
                    self.lastChar -= 4
                elif blockText.startswith('\t'):
                    blockText = blockText[1:]
                    self.lastChar -= 1

            elif mode == 'indent':
                blockText = ' '*4 + blockText
                self.lastChar += 4

            text.append(blockText)

        return text

    #--------------------------------------------------------------------------------------------------
    #current line hightlighting
    #--------------------------------------------------------------------------------------------------

    def highlightCurrentLine(self):
        '''
        Highlight currently selected line
        '''
        extraSelections = []

        selection = QtGuiWidgets.QTextEdit.ExtraSelection()

        lineColor = QtGui.QColor(62, 62, 62, 255)

        selection.format.setBackground(lineColor)
        selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

class KSLineNumberArea(QtGuiWidgets.QWidget):
    def __init__(self, scriptEditor):
        super(KSLineNumberArea, self).__init__(scriptEditor)

        self.scriptEditor = scriptEditor
        self.setStyleSheet("text-align: center;")

    def paintEvent(self, event):
        self.scriptEditor.lineNumberAreaPaintEvent(event)
        return

class KSScriptEditorHighlighter(QtGui.QSyntaxHighlighter):
    '''
    Modified, simplified version of some code found I found when researching:
    wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
    They did an awesome job, so credits to them. I only needed to make some
    modifications to make it fit my needs.
    '''

    def __init__(self, document):

        super(KSScriptEditorHighlighter, self).__init__(document)

        self.styles = {
            'keyword': self.format([238,117,181],'bold'),
            'string': self.format([242, 136, 135]),
            'comment': self.format([143, 221, 144 ]),
            'numbers': self.format([174, 129, 255])
            }

        self.keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'yield'
            ]

        self.operatorKeywords = [
            '=','==', '!=', '<', '<=', '>', '>=',
            '\+', '-', '\*', '/', '//', '\%', '\*\*',
            '\+=', '-=', '\*=', '/=', '\%=',
            '\^', '\|', '\&', '\~', '>>', '<<'
            ]

        self.numbers = ['True','False','None']

        self.tri_single = (QtCore.QRegExp("'''"), 1, self.styles['comment'])
        self.tri_double = (QtCore.QRegExp('"""'), 2, self.styles['comment'])

        #rules
        rules = []

        rules += [(r'\b%s\b' % i, 0, self.styles['keyword']) for i in self.keywords]
        rules += [(i, 0, self.styles['keyword']) for i in self.operatorKeywords]
        rules += [(r'\b%s\b' % i, 0, self.styles['numbers']) for i in self.numbers]

        rules += [

            # integers
            (r'\b[0-9]+\b', 0, self.styles['numbers']),
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['string']),
            # From '#' until a newline
            (r'#[^\n]*', 0, self.styles['comment']),
            ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    def format(self,rgb, style=''):
        '''
        Return a QtGuiWidgets.QTextCharFormat with the given attributes.
        '''

        color = QtGui.QColor(*rgb)
        textFormat = QtGui.QTextCharFormat()
        textFormat.setForeground(color)

        if 'bold' in style:
            textFormat.setFontWeight(QtGui.QFont.Bold)
        if 'italic' in style:
            textFormat.setFontItalic(True)

        return textFormat

    def highlightBlock(self, text):
        '''
        Apply syntax highlighting to the given block of text.
        '''
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        '''
        Check whether highlighting reuires multiple lines.
        '''
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False


#---------------------------------------------------------------------
# Preferences Panel
#---------------------------------------------------------------------
class KnobScripterPrefs(QtGuiWidgets.QDialog):
    def __init__(self, knobScripter):
        super(KnobScripterPrefs, self).__init__()

        # Vars
        self.knobScripter = knobScripter
        self.prefs_txt = self.knobScripter.prefs_txt
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.oldFontSize = self.knobScripter.scriptEditorFont.pointSize()
        self.oldDefaultW = self.knobScripter.windowDefaultSize[0]
        self.oldDefaultH = self.knobScripter.windowDefaultSize[1]

        # Widgets
        kspTitle = QtGuiWidgets.QLabel("KnobScripter v" + version)
        kspTitle.setStyleSheet("font-weight:bold;color:#CCCCCC;font-size:24px;")
        kspSubtitle = QtGuiWidgets.QLabel("Script editor for python and callback knobs")
        kspSubtitle.setStyleSheet("color:#999")
        kspLine = QtGuiWidgets.QFrame()
        kspLine.setFrameShape(QtGuiWidgets.QFrame.HLine)
        kspLine.setFrameShadow(QtGuiWidgets.QFrame.Sunken)
        kspLine.setLineWidth(0)
        kspLine.setMidLineWidth(1)
        kspLine.setFrameShadow(QtGuiWidgets.QFrame.Sunken)
        kspLineBottom = QtGuiWidgets.QFrame()
        kspLineBottom.setFrameShape(QtGuiWidgets.QFrame.HLine)
        kspLineBottom.setFrameShadow(QtGuiWidgets.QFrame.Sunken)
        kspLineBottom.setLineWidth(0)
        kspLineBottom.setMidLineWidth(1)
        kspLineBottom.setFrameShadow(QtGuiWidgets.QFrame.Sunken)
        kspSignature = QtGuiWidgets.QLabel('<a href="http://www.adrianpueyo.com/" style="color:#888;text-decoration:none"><b>adrianpueyo.com</b></a>, 2017-2018')
        kspSignature.setOpenExternalLinks(True)
        kspSignature.setStyleSheet('''color:#555;font-size:9px;''')
        kspSignature.setAlignment(QtCore.Qt.AlignRight)


        fontSizeLabel = QtGuiWidgets.QLabel("Font size:")
        self.fontSizeBox = QtGuiWidgets.QSpinBox()
        self.fontSizeBox.setValue(self.oldFontSize)
        self.fontSizeBox.setMinimum(6)
        self.fontSizeBox.setMaximum(100)
        self.fontSizeBox.valueChanged.connect(self.fontSizeChanged)

        windowWLabel = QtGuiWidgets.QLabel("Width (px):")
        windowWLabel.setToolTip("Default window width in pixels")
        self.windowWBox = QtGuiWidgets.QSpinBox()
        self.windowWBox.setValue(self.knobScripter.windowDefaultSize[0])
        self.windowWBox.setMinimum(200)
        self.windowWBox.setMaximum(4000)
        self.windowWBox.setToolTip("Default window width in pixels")

        windowHLabel = QtGuiWidgets.QLabel("Height (px):")
        windowHLabel.setToolTip("Default window height in pixels")
        self.windowHBox = QtGuiWidgets.QSpinBox()
        self.windowHBox.setValue(self.knobScripter.windowDefaultSize[1])
        self.windowHBox.setMinimum(100)
        self.windowHBox.setMaximum(2000)
        self.windowHBox.setToolTip("Default window height in pixels")


        self.buttonBox = QtGuiWidgets.QDialogButtonBox(QtGuiWidgets.QDialogButtonBox.Ok | QtGuiWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.savePrefs)
        self.buttonBox.rejected.connect(self.cancelPrefs)

        # Loaded custom values
        self.ksPrefs = self.knobScripter.loadPrefs()
        if self.ksPrefs != []:
            try:
                self.fontSizeBox.setValue(self.ksPrefs['font_size'])
                self.windowWBox.setValue(self.ksPrefs['window_default_w'])
                self.windowHBox.setValue(self.ksPrefs['window_default_h'])
            except:
                pass

        # Layouts
        fontSize_layout = QtGuiWidgets.QHBoxLayout()
        fontSize_layout.addWidget(fontSizeLabel)
        fontSize_layout.addWidget(self.fontSizeBox)

        windowW_layout = QtGuiWidgets.QHBoxLayout()
        windowW_layout.addWidget(windowWLabel)
        windowW_layout.addWidget(self.windowWBox)

        windowH_layout = QtGuiWidgets.QHBoxLayout()
        windowH_layout.addWidget(windowHLabel)
        windowH_layout.addWidget(self.windowHBox)

        master_layout = QtGuiWidgets.QVBoxLayout()
        master_layout.addWidget(kspTitle)
        master_layout.addWidget(kspSignature)
        master_layout.addWidget(kspLine)
        master_layout.addLayout(fontSize_layout)
        master_layout.addLayout(windowW_layout)
        master_layout.addLayout(windowH_layout)
        master_layout.addWidget(self.buttonBox)
        self.setLayout(master_layout)
        self.setFixedSize(self.minimumSize())

    def savePrefs(self):
        ks_prefs = {
            'font_size': self.fontSizeBox.value(),
            'window_default_w': self.windowWBox.value(),
            'window_default_h': self.windowHBox.value()
        }
        self.knobScripter.scriptEditorScript.setFont(self.knobScripter.scriptEditorFont)
        with open(self.prefs_txt,"w") as f:
            prefs = json.dump(ks_prefs, f)
            self.accept()
        return prefs

    def cancelPrefs(self):
        self.knobScripter.scriptEditorFont.setPointSize(self.oldFontSize)
        self.knobScripter.scriptEditorScript.setFont(self.knobScripter.scriptEditorFont)
        self.reject()

    def fontSizeChanged(self):
        self.knobScripter.scriptEditorFont.setPointSize(self.fontSizeBox.value())
        self.knobScripter.scriptEditorScript.setFont(self.knobScripter.scriptEditorFont)
        return

    def closeEvent(self,event):
        self.cancelPrefs()
        self.close()


def showKnobScripter(knob="knobChanged"):
    selection = nuke.selectedNodes()
    if not len(selection):
        nuke.message("Please select one or more nodes!")
    else:
        if len(selection) > 1:
            nuke.message("More than one node selected.\nOpening knobChanged editor for %s" % selection[0].name())
        pan = KnobScripter(selection[0], knob)
        pan.show()


def addKnobScripterPanel():
    global knobScripterPanel
    try:
        knobScripterPanel = panels.registerWidgetAsPanel(moduleName + 'KnobScripterPane', 'Knob Scripter',
                                     'com.adrianpueyo.KnobScripterPane')
        knobScripterPanel.addToPane(nuke.getPaneFor('Properties.1'))

    except:
        knobScripterPanel = panels.registerWidgetAsPanel(moduleName + 'KnobScripterPane', 'Knob Scripter', 'com.adrianpueyo.KnobScripterPane')

moduleName = __name__
if moduleName == '__main__':
  moduleName = ''
else:
  moduleName = moduleName + '.'

ksShortcut = "alt+z"
addKnobScripterPanel()
nuke.menu('Nuke').addCommand('Edit/Node/Open Floating Knob Scripter', showKnobScripter, ksShortcut)