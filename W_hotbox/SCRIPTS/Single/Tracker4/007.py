#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: TrackConnect
#
#----------------------------------------------------------------------------------------------------------

def main():
    import nuke
    import nukescripts
    import nuke.rotopaint as rp
    
    class TrackConnect(nukescripts.PythonPanel):
        """
        Creates a Nuke Panel called TrackConnect.
    
        Allows the individual selection of translation, rotation
        and scale with the option to bake or parent the tracking
        data into the node.
    
        Creates a new Roto or RotoPaint node with tracking attached
        to a new layer in the node.
        """
    
        def __init__(self, trkNode):
            nukescripts.PythonPanel.__init__(self, 'TrackConnect', 'org.magpie.trackconnect')
    
            # INSTANCE VARIABLES
    
            # trkNode-specific instance variables ##
            self.trkNode = trkNode
            self.trkNode_Name = trkNode.name()
            # assign tracker variables #
            self.trkNode_transExp = 'parent.' + self.trkNode_Name + '.translate'
            self.trkNode_rotateExp = 'parent.' + self.trkNode_Name + '.rotate'
            self.trkNode_scaleExp = 'parent.' + self.trkNode_Name + '.scale'
            self.trkNode_centerExp = 'parent.' + self.trkNode_Name + '.center'
            # trkNode attributes
            self.trkNode_transVals = trkNode['translate']
            self.trkNode_rotVal = trkNode['rotate']
            self.trkNode_scaleVals = trkNode['scale']
            self.trkNode_centerVals = trkNode['center']
    
            # CREATE KNOBS
    
            # dividers
            self.div1 = nuke.Text_Knob('div1', '', '')
            self.div2 = nuke.Text_Knob('div2', '', '')
            self.div3 = nuke.Text_Knob('div3', '', '')
            self.div4 = nuke.Text_Knob('div4', '', '')
            # check boxes
            self.transBox = nuke.Boolean_Knob('trans', 'translate')
            self.rotBox = nuke.Boolean_Knob('rot', 'rotate')
            self.scaleBox = nuke.Boolean_Knob('scale', 'scale')
            # text
            self.text = nuke.Text_Knob("toolName", "TrackConnect -",
                                       "Create a roto node based on tracking data from " + self.trkNode_Name)
            self.checkText = nuke.Text_Knob("", "relevant data:", self.trkNode_transExp + ", " + self.trkNode_rotateExp)
            # pulldown selection box
            self.enumKnobNodeType = nuke.Enumeration_Knob('my choices', 'Node Type', ['Roto', 'RotoPaint'])
            self.enumKnobMethod = nuke.Enumeration_Knob('my choices', '             Method', ['Parent', 'Bake'])
            # keep pull-downs on same line
            self.enumKnobMethod.clearFlag(nuke.STARTLINE)
            # add button #
            self.execute = nuke.PyScript_Knob("", "Execute", "")
            # populate knob list #
            self.knobSet = [self.text, self.div1, self.enumKnobNodeType, self.enumKnobMethod,
                            self.div2, self.transBox, self.rotBox,
                            self.scaleBox, self.div3, self.execute]
            # add knobs #
            for knob in range(len(self.knobSet)):
                self.addKnob(self.knobSet[knob])
    
            # add cancel button #
            if self.cancelButton is None:
                self.cancelButton = nuke.Script_Knob("Cancel")
                self.addKnob(self.cancelButton)
    
            # disable checkbox(es) if no tracking data exists
            if not self.trkNode['translate'].isAnimated():
                self.transBox.setEnabled(False)
            else:
                self.transBox.setValue(True)

            if not self.trkNode['rotate'].isAnimated():
                self.rotBox.setEnabled(False)
            else:
                self.rotBox.setValue(True)

            if not self.trkNode['scale'].isAnimated():
                self.scaleBox.setEnabled(False)
            else:
                self.scaleBox.setValue(True)
        # end __INIT__
    
        ####################################################
        # Parent translate data from tracker to roto node ##
        ####################################################
        def parentTranslate(self, rotoLayer, tracker_transExp):
            # parents tracker to root translate x
            rotoLayer.getTransform().getTranslationAnimCurve(0).expressionString = tracker_transExp
            rotoLayer.getTransform().getTranslationAnimCurve(0).useExpression = True
            # parents tracker to root translate y
            rotoLayer.getTransform().getTranslationAnimCurve(1).expressionString = tracker_transExp
            rotoLayer.getTransform().getTranslationAnimCurve(1).useExpression = True
        # end parentTranslate()
    
        #################################################
        # Parent rotate data from tracker to roto node ##
        #################################################
        def parentRotate(self, rotoLayer, tracker_rotExp):
            # parents tracker to root rotate curve
            rotoLayer.getTransform().getRotationAnimCurve(2).expressionString = tracker_rotExp
            rotoLayer.getTransform().getRotationAnimCurve(2).useExpression = True
        # end parentRotate()
    
        ################################################
        # Parent scale data from tracker to roto node ##
        ################################################
        def parentScale(self, rotoLayer, tracker_scaleExp):
            # parents tracker to root scale x and y
            rotoLayer.getTransform().getScaleAnimCurve(0).expressionString = tracker_scaleExp
            rotoLayer.getTransform().getScaleAnimCurve(1).expressionString = tracker_scaleExp
            # execute
            rotoLayer.getTransform().getScaleAnimCurve(0).useExpression = True
            rotoLayer.getTransform().getScaleAnimCurve(1).useExpression = True
        # end parentScale()
    
        ######################################################
        # Parent pivot point data from tracker to roto node ##
        ######################################################
        def parentPivotPoint(self, rotoLayer, tracker_centerExp):
            # parents tracker to root pivot point x
            rotoLayer.getTransform().getPivotPointAnimCurve(0).expressionString = tracker_centerExp
            rotoLayer.getTransform().getPivotPointAnimCurve(0).useExpression = True
            # parents tracker to root pivot point y
            rotoLayer.getTransform().getPivotPointAnimCurve(1).expressionString = tracker_centerExp
            rotoLayer.getTransform().getPivotPointAnimCurve(1).useExpression = True
        # end parentPivotPoint()
    
        ##################################################
        # Bake translate data from tracker to roto node ##
        ##################################################
        def bakeTranslate(self, rotoLayer, trkNode_transVals):
            self.firstFrame = nuke.root().firstFrame()
            self.lastFrame = nuke.root().lastFrame()
            for frame in range(self.firstFrame, self.lastFrame + 1):
                self.trkNode_xTransVal = trkNode_transVals.getValueAt(frame)[0]
                self.trkNode_yTransVal = trkNode_transVals.getValueAt(frame)[1]
                rotoLayer.getTransform().getTranslationAnimCurve(0).addKey(frame, self.trkNode_xTransVal)
                rotoLayer.getTransform().getTranslationAnimCurve(1).addKey(frame, self.trkNode_yTransVal)
        # end bakeTranslate()
    
        ###############################################
        # Bake rotate data from tracker to roto node ##
        ###############################################
        def bakeRotate(self, rotoLayer, trkNode_rotVal):
            self.firstFrame = nuke.root().firstFrame()
            self.lastFrame = nuke.root().lastFrame()
            for frame in range(self.firstFrame, self.lastFrame + 1):
                self.trkNode_rVal = trkNode_rotVal.getValueAt(frame)
                rotoLayer.getTransform().getRotationAnimCurve(2).addKey(frame, self.trkNode_rVal)
        # end bakeRotate()
    
        ##############################################
        # Bake scale data from tracker to roto node ##
        ##############################################
        def bakeScale(self, rotoLayer, trkNode_scaleVals):
            self.firstFrame = nuke.root().firstFrame()
            self.lastFrame = nuke.root().lastFrame()
            for frame in range(self.firstFrame, self.lastFrame + 1):
                try:
                    self.trkNode_xScaleVal = trkNode_scaleVals.getValueAt(frame)[0]
                    self.trkNode_yScaleVal = trkNode_scaleVals.getValueAt(frame)[1]
                    rotoLayer.getTransform().getScaleAnimCurve(0).addKey(frame, self.trkNode_xScaleVal)
                    rotoLayer.getTransform().getScaleAnimCurve(1).addKey(frame, self.trkNode_yScaleVal)
                except:
                    self.trkNode_scaleVal = trkNode_scaleVals.getValueAt(frame)
                    rotoLayer.getTransform().getScaleAnimCurve(0).addKey(frame, self.trkNode_scaleVal)
                    rotoLayer.getTransform().getScaleAnimCurve(1).addKey(frame, self.trkNode_scaleVal)
        # end bakeScale()
    
        ####################################################
        # Bake pivot point data from tracker to roto node ##
        ####################################################
        def bakePivotPoint(self, rotoLayer, trkNode_centerVals):
            self.firstFrame = nuke.root().firstFrame()
            self.lastFrame = nuke.root().lastFrame()
            for frame in range(self.firstFrame, self.lastFrame + 1):
                self.trkNode_xPpVal = trkNode_centerVals.getValueAt(frame)[0]
                self.trkNode_yPpVal = trkNode_centerVals.getValueAt(frame)[1]
                rotoLayer.getTransform().getPivotPointAnimCurve(0).addKey(frame, self.trkNode_xPpVal)
                rotoLayer.getTransform().getPivotPointAnimCurve(1).addKey(frame, self.trkNode_yPpVal)
        # end bakePivotPoint()
    
        ######################################
        # create roto node with tracker data #
        ######################################
        def create_RotoNode(self):
            # create new roto node
            if self.enumKnobNodeType.value() == 'RotoPaint':
                self.rNode = nuke.nodes.RotoPaint()
                # set output to rgba
                self.rNode['output'].setValue('rgba')
            else:
                self.rNode = nuke.nodes.Roto()
                # set output to alpha
                self.rNode['output'].setValue('alpha')
            self.rCurves = self.rNode['curves']
            self.root = self.rCurves.rootLayer
            self.layer = rp.Layer(self.rCurves)
            # create new layer
            self.root.append(self.layer)
    
            # set node position
            self.rNode.setXpos(self.trkNode.xpos())  # set x
            self.rNode.setYpos(self.trkNode.ypos() + self.trkNode.screenHeight() + 15)  # set y
    
    
            if self.transBox.value() == True:
                if self.enumKnobMethod.value() == 'Parent':
                    self.parentTranslate(self.root[0], self.trkNode_transExp)
                else:  # run bake method for translate
                    self.bakeTranslate(self.root[0], self.trkNode_transVals)
            if self.rotBox.value() == True:
                if self.enumKnobMethod.value() == 'Parent':
                    self.parentRotate(self.root[0], self.trkNode_rotateExp)
                else:  # run bake method for rotate
                    self.bakeRotate(self.root[0], self.trkNode_rotVal)
            if self.scaleBox.value() == True:
                if self.enumKnobMethod.value() == 'Parent':
                    self.parentScale(self.root[0], self.trkNode_scaleExp)
                else:  # run bake method for scale
                    self.bakeScale(self.root[0], self.trkNode_scaleVals)
            # run pivot no matter what
            if self.enumKnobMethod.value() == 'Parent':
                self.parentPivotPoint(self.root[0], self.trkNode_centerExp)
            else:  # run bake method for pp
                self.bakePivotPoint(self.root[0], self.trkNode_centerVals)
    
            if self.enumKnobMethod.value() == 'Parent':
                print(self.rNode.name() + ' has parented tracking data from ' + self.trkNode_Name)
            else:
                print(self.rNode.name() + ' has baked tracking data from ' + self.trkNode_Name)
            # return roto node
            return self.rNode
        # end create_RotoNode()
    
        #####################################
        # check to see if a knob is changed #
        #####################################
        def knobChanged(self, knob):
            if knob is self.execute:
                # If no box is checked, verify that this is correct.
                if self.isChecked() == False:
                    query = nuke.ask(
                        "No boxes selected.\nA roto node with a tracked pivot will be created.\nIs that what you want?")
                    print query
                    if query == True:
                        self.create_RotoNode()
                        # close panel
                        self.finishModalDialog(True)
                else:
                    self.create_RotoNode()
                    # close panel
                    self.finishModalDialog(True)
        # end knobChanged()
    
        ###################################
        # verify if any boxes are checked #
        ###################################
        def isChecked(self):
            # Return False if no box is checked, True if any/all box(es) is(are) checked
            if (self.transBox.value() != True and self.rotBox.value() != True and self.scaleBox.value() != True):
                return False
            else:
                return True
        # end isChecked()
    # end TrackConnect
    
    ####################################
    # Create TrackConnect Dialog Panel #
    ####################################
    def create_TCPanel():
        try:
            trkNode = nuke.selectedNode()
            if trkNode.Class() != 'Tracker4':
                nuke.message('Not a tracker node. Please select your Tracker node')
                return
            elif trkNode['tracks'].getValue() == 0.0:
                nuke.message('There are no trackers present in Tracker node')
                return
            else:
                t = TrackConnect(trkNode)
                return t.showModal()
        except ValueError:
            nuke.message('please select a tracking node')
    # end create_TCPanel()
    create_TCPanel()
main()
