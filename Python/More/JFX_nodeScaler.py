##########################################################################
# JFX_nodeScaler v1.0, 2014-10-31
# by Justin Gros-Desir, http://justin-vfx.com
#
#
#						 Nodes Scale
#	      Scale the distance between selected nodes
#
#
# In your menu.py :
#
#   import JFX_nodeScaler
# 	mNuke = nuke.menu("Nuke")
# 	mMenu = mNuke.addMenu("MyMenu")
# 	mMenu.addCommand('JFX_nodeScaler', JFX_nodeScaler.ScaleNodes)
#
# or using JFX_utils.py , just paste this file anywhere in your .nuke/ nothing else...
#
#
#				
##########################################################################

import nuke
import nukescripts
import operator
import copy
import os


if nuke.env["gui"]:
	class ScaleNodes(object):
		def __init__(self, parent=None):
			self._parent = parent
			self.scale_nodes()

		def scale_nodes(self):
		    'Call the class'
		    p = ScaleNodesPanel()
		    return p.showModalDialog()



	class ScaleNodesPanel(nukescripts.PythonPanel):
		'''
		    Main tool's class
		'''
		def __init__(self):
			nukescripts.PythonPanel.__init__( self, "Scale the distance between selected nodes", 'justin-vfx.com')
			self.setMinimumSize(500, 150)

			self.uniform = nuke.Boolean_Knob('uniform','uniform scale')
			self.uniform.setValue(True)

			self.push = nuke.Boolean_Knob('push','push other nodes when scaling up')
			self.push.setValue(False)
			self.push.clearFlag(nuke.STARTLINE)
			self.scale = nuke.Double_Knob( "scale", "scale" )
			self.scale.setRange(0,10)
			self.scale.setValue(1)

			self.scaleX = nuke.Double_Knob( "scalex", "width" )
			self.scaleX.setRange(0,10)
			self.scaleX.setValue(1)
			self.scaleX.setVisible(False)

			self.scaleY = nuke.Double_Knob( "scaley", "height" )
			self.scaleY.setRange(0,10)
			self.scaleY.setValue(1)
			self.scaleY.setVisible(False)

			self.addKnob( self.uniform )
			self.addKnob( self.push )
			self.addKnob( self.scale )
			self.addKnob( self.scaleX )
			self.addKnob( self.scaleY )
			self.addKnob(nuke.Text_Knob(''))

			self.XMaxFirstNeedToPush = True
			self.XMinFirstNeedToPush = True
			self.YMaxFirstNeedToPush = True
			self.YMinFirstNeedToPush = True
			self.nToPushXMaxOrigPos_dic = {}
			self.nToPushXMinOrigPos_dic = {}
			self.nToPushYMaxOrigPos_dic = {}
			self.nToPushYMinOrigPos_dic = {}
			self.origDic = {}
			self.n_dic = {}
			self.needToPush = False

			self.ops = {
					"+": operator.add,
					"-": operator.sub,
					"<": operator.lt,
					"<=": operator.le,
					">": operator.gt,
					">=": operator.ge
					}

			nodes = nuke.allNodes()
			self.selectedNodes = nuke.selectedNodes()

			for n in nodes:
				origXpos = n.xpos()
				origYpos = n.ypos()
				if n.Class() == 'BackdropNode':
					self.n_dic[n]=[origXpos+n['bdwidth'].value()/2,
						           origYpos+n['bdheight'].value()/2,
						           n['bdwidth'].value(),n['bdheight'].value()]
				else:
					self.n_dic[n]=[origXpos+n.screenWidth()/2,origYpos+n.screenHeight()/2]

			nuke.addKnobChanged(self.knobChanged)


		def knobChanged(self, knob=None):
		  '''
		  Callbacks methodes
		  '''
		  knob = nuke.thisKnob()
		  if knob.name() == 'scale':
		      self.scaleNodes(self.scale.value(),self.scale.value())
		  if knob.name() == 'uniform':
		      self.scaleX.setVisible(not knob.value())
		      self.scaleY.setVisible(not knob.value())
		      self.scale.setVisible(knob.value())
		  if knob.name() == 'scalex' or knob.name() == 'scaley':
		      self.scaleNodes(self.scaleX.value(),self.scaleY.value())

		  if knob.name() == 'push':
		          self.needToPush = knob.value()


		def scaleNodes(self, scaleX, scaleY ):
		    '''
		    Process the scaling
		    '''
		    listX = []
		    listY = []
		    amount = len( self.selectedNodes )
		    if amount == 0:    return

		    for n in self.selectedNodes:
		        for key, values in self.n_dic.iteritems():
		            if n == key:
		                origXpos = values[0]
		                origYpos = values[1]

		                listX.append(origXpos)
		                listY.append(origYpos)

		    allX = sum(listX)
		    allY = sum(listY)

		    # CENTER OF SELECTED NODES
		    centreX = allX / amount
		    centreY = allY / amount


		    nodesXSup = []

		    # Scaling algo
		    for n in self.selectedNodes:
		        if n == self.selectedNodes[0]:
		            xMin = xMax = n.xpos() + n.screenWidth()/2
		            yMin = yMax = n.ypos() + n.screenHeight()/2
		        for key, values in self.n_dic.iteritems():
		            if n == key:
		                origXpos = values[0]
		                origYpos = values[1]
		                nCenterX = n.screenWidth()/2
		                nCenterY = n.screenHeight()/2
		                if n.Class() == 'BackdropNode':
		                    bdW = values[2]
		                    bdH = values[3]

		                    n['bdwidth'].setValue(bdW * scaleX)
		                    n['bdheight'].setValue(bdH * scaleY)
		                    nCenterX = n['bdwidth'].value()/2
		                    nCenterY = n['bdheight'].value()/2


		                n.setXpos( int(round((centreX-nCenterX)+ ( origXpos - centreX ) * scaleX)))
		                n.setYpos( int(round((centreY-nCenterY)+ ( origYpos - centreY ) * scaleY)))

		                if n.Class() == 'BackdropNode':
		                    if (n.xpos() + n['bdwidth'].value()/2) > xMax:
		                        xMax =  n.xpos() + n['bdwidth'].value()/2
		                    elif(n.xpos() + n['bdwidth'].value()/2) < xMin:
		                        xMin =  n.xpos() + n['bdwidth'].value()/2

		                    if (n.ypos() + n['bdheight'].value()/2) > yMax:
		                        yMax =  n.ypos() + n['bdheight'].value()/2
		                    elif (n.ypos() + n['bdheight'].value()/2) < yMin:
		                        yMin =  n.ypos() + n['bdheight'].value()/2
		                else:
		                    if (n.xpos() + n.screenWidth()/2) > xMax:
		                        xMax =  n.xpos() + n.screenWidth()/2
		                    elif(n.xpos() + n.screenWidth()/2) < xMin:
		                        xMin =  n.xpos() + n.screenWidth()/2

		                    if (n.ypos() + n.screenHeight()/2) > yMax:
		                        yMax =  n.ypos() + n.screenHeight()/2
		                    elif (n.ypos() + n.screenHeight()/2) < yMin:
		                        yMin =  n.ypos() + n.screenHeight()/2

		    if self.needToPush:
		        if self.XMaxFirstNeedToPush:
		            self.origDic = self.nToPushXMaxOrigPos_dic
		            if not self.firstNodeXtoPush(xMax,"+",">","<="):self.XMaxFirstNeedToPush = False
		        else:
		            self.origDic = self.nToPushXMaxOrigPos_dic
		            self.pushNodesX(xMax,"+",">","<=")

		        if self.XMinFirstNeedToPush:
		            self.origDic = self.nToPushXMinOrigPos_dic
		            if not self.firstNodeXtoPush(xMin,"-","<",">="):self.XMinFirstNeedToPush = False
		        else:
		            self.origDic = self.nToPushXMinOrigPos_dic
		            self.pushNodesX(xMin,"-","<",">=")

		        if self.YMaxFirstNeedToPush:
		            self.origDic = self.nToPushYMaxOrigPos_dic
		            if not self.firstNodeYtoPush(yMax, "+", ">", "<="):self.YMaxFirstNeedToPush = False
		        else:
		            self.origDic = self.nToPushYMaxOrigPos_dic
		            self.pushNodesY(yMax, "+", ">", "<=")

		        if self.YMinFirstNeedToPush:
		            self.origDic = self.nToPushYMinOrigPos_dic
		            if not self.firstNodeYtoPush(yMin, "-", "<", ">="):self.YMinFirstNeedToPush = False
		        else:
		            self.origDic = self.nToPushYMinOrigPos_dic
		            self.pushNodesY(yMin, "-", "<", ">=")


		def firstNodeXtoPush(self, xMinOrMax, opAddOrSub,opGreaterOrLower,opGreaterEOrLowerE):
		    pushX = False
		    bool = True
		    for key, values in self.n_dic.iteritems():
		        if key not in self.selectedNodes:
		            if (self.ops[opGreaterOrLower](key.xpos()+ key.screenWidth()/2, xMinOrMax) and
		                self.ops[opGreaterEOrLowerE](key.xpos()+ key.screenWidth()/2, self.ops[opAddOrSub](xMinOrMax, 100))):#val abs la aussi?
		                pushX = True
		    if pushX:
		        for key, values in self.n_dic.iteritems():
		            if key not in self.selectedNodes:
		                if self.ops[opGreaterOrLower](key.xpos()+ key.screenWidth()/2, xMinOrMax):
		                    self.origDic[key] = [abs(values[0]-xMinOrMax)]
		                    bool = False
		        pushX = False
		    return bool

		def pushNodesX(self,xMinOrMax,opAddOrSub,opGreaterOrLower,opGreaterEOrLowerE):
		    for n, values in self.origDic.iteritems():
		            for key in self.n_dic.keys():
		                if n == key:
		                    if self.ops[opGreaterOrLower](self.ops[opAddOrSub](xMinOrMax, values[0]), key.xpos()+ key.screenWidth()/2):
		                        n.setXpos(int(self.ops[opAddOrSub](xMinOrMax, values[0])-key.screenWidth()/2))


		def firstNodeYtoPush(self, yMinOrMax, opAddOrSub,opGreaterOrLower,opGreaterEOrLowerE):
		    pushY = False
		    bool = True
		    for key, values in self.n_dic.iteritems():
		        if key not in self.selectedNodes:
		            if (self.ops[opGreaterOrLower](key.ypos()+ key.screenHeight()/2, yMinOrMax) and
		                self.ops[opGreaterEOrLowerE](key.ypos()+ key.screenHeight()/2, self.ops[opAddOrSub](yMinOrMax, 100))):#val abs la aussi?
		                pushY = True
		    if pushY:
		        for key, values in self.n_dic.iteritems():
		            if key not in self.selectedNodes:
		                if self.ops[opGreaterOrLower](key.ypos()+ key.screenHeight()/2, yMinOrMax):
		                    self.origDic[key] = [abs(values[1]-yMinOrMax)]
		                    bool = False
		        pushY = False
		    return bool

		def pushNodesY(self,yMinOrMax,opAddOrSub,opGreaterOrLower,opGreaterEOrLowerE):
		    for n, values in self.origDic.iteritems():
		            for key in self.n_dic.keys():
		                if n == key:
		                    if self.ops[opGreaterOrLower](self.ops[opAddOrSub](yMinOrMax, values[0]), key.ypos()+ key.screenHeight()/2):
		                        n.setYpos(int(self.ops[opAddOrSub](yMinOrMax, values[0])-key.screenHeight()/2))



		def showModalDialog( self ):
		    '''
		    Show the panel
		    '''
		    result = nukescripts.PythonPanel.showModalDialog( self )
		    nuke.removeKnobChanged(self.knobChanged)
		    if  not result:
		        nodes = nuke.allNodes()
		        for n in nodes:
		            for key, values in self.n_dic.iteritems():
		                if n == key:
		                    if n.Class() == 'BackdropNode':
		                        n['bdwidth'].setValue(values[2])
		                        n['bdheight'].setValue(values[3])
		                        n.setXYpos(int(values[0]- key['bdwidth'].value()/2),int(values[1]- key['bdheight'].value()/2))

		                    else:
		                        n.setXYpos(int(values[0])- key.screenWidth()/2,int(values[1])- key.screenHeight()/2)
		        return


	def setCommands(pythonTools):
		pythonTools.addCommand( 'JFX_nodeScaler', ScaleNodes, 'shift+l' )




