

import nuke
import nukescripts
import os
import thread
import platform
import subprocess
import webbrowser

capturedImages = []
capturedNodes = []
capturedImagesBtn = []
capturedNodesBtn = []
dontInclude=[".DS_Store"]

def openFileReturnArr(file):
	'''
	open set file, read in all lines and
	return an array with all the lines
	'''

	arr=[]
	fobj = open("%s"%file, "r")
	#load in all lines
	for line in fobj:
		#delete word wrap at the end of each line
		line=line.replace("\n", "")
		arr.append(line)
	fobj.close()
	return arr

def getSetting(settingsFile, val):
	'''
	getValues by finding pattern in array.
	for getting the values out of the array which
	comes from the settings text file
	'''

	arr = openFileReturnArr(settingsFile)
	i=0
	for line in arr:
		findVal=arr[i].find("%s"%val)
		#if pattern found
		if findVal!=-1:
			val=arr[i]
			valArr=val.split("=")
			try:
				val=valArr[1] #value
				if val=="":
					val=" "
				elif val=="NONE":
					val=" "
			except:
				val="---"
		i+=1
	return val

def initCaptureSettings():
	'''
	read capture settings file or create if not exist
	'''

	global captureImageDir
	global captureNodesDir
	global captureDir
	global captureSettings

	captureDir=os.getenv("HOME")+"/.nuke/capture"
	captureSettings=captureDir+"/captureSettings.txt"

	if not os.path.isdir(captureDir):
		os.makedirs(captureDir)
	if not os.path.isfile(captureSettings):
		rs = open(captureSettings,'w+')
		rs.write("@captureImageDir=%s/capturedImages\n" % captureDir )
		rs.write("@captureNodesDir=%s/capturedNodes\n" % captureDir )
		rs.close()	
		os.makedirs("%s/capturedImages" % captureDir)
		os.makedirs("%s/capturedNodes" % captureDir)

	else:
		rs=open(captureSettings,'r+')
		rs.close()

	captureImageDir=getSetting(captureSettings,"@captureImageDir")
	captureNodesDir=getSetting(captureSettings,"@captureNodesDir")

def initCapture(which):
	'''
	create captureImageDir if not exist, load buttons into stack
	'''
	global capturedImagesBtn
	global capturedNodesBtn

	capturedImagesBtn = []
 	capturedNodesBtn= []

	if which == "images":
		global capturedImages
		capturedImages=[]

		#force create captureImageDir
		if not os.path.isdir(captureImageDir):
			os.makedirs(captureImageDir)

		#init all saved images
		for cap in os.listdir(captureImageDir):
			if cap not in dontInclude:
				capturedImages.append(cap)

	if which == "nodes":
		global capturedNodes
		capturedNodes=[]
	
		#force create captureNodesDir
		if not os.path.isdir(captureNodesDir):
			os.makedirs(captureNodesDir)

		#init all saved nodes
		for capN in os.listdir(captureNodesDir):
			if capN not in dontInclude:
				capturedNodes.append(capN)

def captureSettingsPanel():
	'''
	panel to edit capture settings
	'''
	
	global captureImageDir
	global captureNodesDir

	initCaptureSettings()
	p = nuke.Panel("Toolset Settings")
	p.setWidth(600)
	p.addFilenameSearch("Directory", captureNodesDir)
	#p.addFilenameSearch("capture images directory", captureImageDir)

	if p.show():
		#captureImageDir=p.value("capture images directory")
		captureNodesDir=p.value("Directory")
		rs = open(captureSettings,'w+')
		rs.write("@captureImageDir=%s\n" % captureImageDir )
		rs.write("@captureNodesDir=%s\n" % captureNodesDir )

		if not os.path.isdir(captureImageDir):
			os.makedirs(captureImageDir)
		if not os.path.isdir(captureNodesDir):
			os.makedirs(captureNodesDir)

def saveImage(name, panel):
	'''
	write image to captureImageDir
	'''

	sel = nuke.selectedNodes()
	
	try:
		c = os.path.dirname(captureImageDir)+"/%s.png" % name
		if os.path.isfile(c):
			if nuke.ask("'%s' already exists. Overwrite it?" % name):
				#delete old button
				for c in capturedImagesBtn:
					if c.name() == name:
						panel.removeKnob(c)
						capturedImagesBtn.remove(c)
				thread.start_new_thread(captureImage, (name, sel))
			else:
				pass
		else:
			thread.start_new_thread(captureImage, (name, sel))
	except:
		nuke.message("Error writing file")

	capturedImages.append("%s.png" % name)

def saveNodes(name, panel):
	'''
	write selected nodes to captureNodesDir
	'''

	try:
		c = captureNodesDir+"/%s.nk" % name
		if os.path.isfile(c):
			if nuke.ask("'%s' already exists. Overwrite it?" % name):
				#delete old button
				for c in capturedNodesBtn:
					if c.name() == name:
						panel.removeKnob(c)
						capturedNodesBtn.remove(c)
				nuke.nodeCopy("{0}/{1}.nk".format(captureNodesDir,name))
			else:
				pass
		else:
			nuke.nodeCopy("{0}/{1}.nk".format(captureNodesDir,name))
	except:
		nuke.message("An error occured while trying to capture the selected nodes.")

def revealDir(which):
	'''
	reveal images or nodes dir in explorer
	'''

	capdir=""
	if which == "images":
		capdir=captureImageDir

	if which == "nodes":
		capdir=captureNodesDir

	if not os.path.isdir(capdir):
		nuke.message("couldn't open the capture %s dir. No such directory." % which)
		return

	try:
		if platform.system() == "Windows":
			os.startfile(capdir)
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", capdir])
		else:
			subprocess.Popen(["xdg-open", capdir])
	except:
		pass
	
def captureImage(name, sel):
	'''
	create write node to capture node
	'''

	def writeFrame(node):
		'''
		write out frame
		'''
		nuke.execute(node,nuke.frame(),nuke.frame())
		nuke.delete(node)

	w = nuke.nodes.Write()
	w.setInput(0,sel[0])
	w.setXpos(sel[0].xpos())
	w.setYpos(sel[0].ypos()+150)
	w.knob("file_type").setValue("png")
	w.knob("file").setValue(os.path.dirname(captureImageDir)+"/%s.png" % name)
	nuke.executeInMainThread(writeFrame, (w)) 
	
def loadImage(img):
	'''
	load image
	'''	
	r = nuke.createNode("Read")
	r["file"].setValue("{0}/{1}.png".format(captureImageDir,img))

def deleteImageCap(panel):
	'''
	delete captured image
	'''	

	p=nuke.Panel('delete capture image')
	p.setWidth(400) 
	toDelete=[]  
	#checkbox for every capture image
	for cBtn in os.listdir(captureImageDir):
		if cBtn not in dontInclude:
			if cBtn[0]==".":
				continue
			p.addBooleanCheckBox(cBtn.replace(".png",""), False)
	#remove all
	p.addBooleanCheckBox("--remove all captured images--", False)

	if p.show():
		#remove all
		if p.value("--remove all captured images--")==True:
			if nuke.ask("Are you sure to delete all captured images? There is NO undo!"):
				#flush toDelete jobs
				for d in toDelete:
					toDelete.remove(d)
				
				for cBtn in capturedImagesBtn:
					panel.removeKnob(cBtn)
					toDelete.append(cBtn)
			else:
				#flush toDelete jobs
				for d in toDelete:
					toDelete.remove(d)
				return

		#remove specific image
		for cBtn in capturedImagesBtn:
			if p.value(cBtn.name())==True:
				panel.removeKnob(cBtn)
				toDelete.append(cBtn)
		
		for d in toDelete:
			try:
				capturedImagesBtn.remove(d)
			except:
				print "could not find knob %s in capturedImagesBtn" %d.name()
			try:
				capturedImages.remove("%s.png" % d.name())
			except:
				print "could not find %s in capturedImages" %d.name()
			try:
				os.remove(captureImageDir+"/%s.png" % d.name())
			except:
				print "could not remove capture image"

		#flush toDelete jobs
		for d in toDelete:
			toDelete.remove(d)

def deleteNodesCap(panel):
	'''
	delete captured nodes
	'''	

	p=nuke.Panel('delete capture nodes')
	p.setWidth(400)   
	toDelete=[]
	#checkbox for every capture image
	for cBtn in os.listdir(captureNodesDir):
		if cBtn not in dontInclude:
			if cBtn[0]==".":
				continue
			p.addBooleanCheckBox(cBtn.replace(".nk",""), False)
	#remove all
	p.addBooleanCheckBox("--remove all capture nodes--", False)

	if p.show():
		#remove all
		if p.value("--remove all capture nodes--")==True:
			if nuke.ask("Are you sure to delete all captured nodes? There is NO undo!"):
				#flush toDelete jobs
				for d in toDelete:
					toDelete.remove(d)
				
				for cBtn in capturedNodesBtn:
					panel.removeKnob(cBtn)
					toDelete.append(cBtn)
			else:
				#flush toDelete jobs
				for d in toDelete:
					toDelete.remove(d)
				return

		#remove specific nodes
		for cBtn in capturedNodesBtn:
			if p.value(cBtn.name())==True:
				panel.removeKnob(cBtn)
				toDelete.append(cBtn)
		
		for d in toDelete:
			try:
				capturedNodesBtn.remove(d)
			except:
				print "could not find knob %s in capturedNodesBtn" %d.name()
			try:
				capturedNodes.remove("%s.nk" % d.name())
			except:
				print "could not find %s in capturedNodes" %d.name()
			try:
				os.remove(captureNodesDir+"/%s.nk" % d.name())
			except:
				print "could not remove capture nodes"

		#flush toDelete jobs
		for d in toDelete:
			toDelete.remove(d)

def initCaptureBtn(option, panel, capList, capBtnList):
	'''
	init buttons for assets in nodes and images capture panel
	'''

	i=0
	for cap in capList:
		
		fileN, fileExt = os.path.splitext(cap)
		
		if option=="images":
			if fileExt!=".png":
				continue
			if fileN[0]==".":
				continue
		if option=="nodes":
			if fileExt!=".nk":
				continue
			if fileN[0]==".":
				continue
		i+=1
		
		panel.capBtn = nuke.PyScript_Knob(fileN, fileN)

		if i%5==0:
			panel.capBtn.setFlag(nuke.STARTLINE)

		panel.addKnob(panel.capBtn)
		capBtnList.append(panel.capBtn)

class captureImagesPanel(nukescripts.PythonPanel):
	'''
	captureImagesPanel
	'''

	def __init__(self):

		initCapture("images")

		nukescripts.PythonPanel.__init__(self, "capture images", "capture images")

		#create elements
		
		'''image tab'''

		self.img_textSave = nuke.Text_Knob( '', 'save/delete', '')
		self.img_name = nuke.String_Knob('name', 'name:')
		self.img_save = nuke.PyScript_Knob('save image', 'save')   
		self.img_delete = nuke.PyScript_Knob('delete image', 'delete')
		self.img_update = nuke.PyScript_Knob('update image', 'update')
		self.img_textCaptured = nuke.Text_Knob( '', 'captured', '')
		self.img_textCaptured.setFlag(nuke.STARTLINE)
		
		#add elements
		self.addKnob(self.img_textSave)
		self.addKnob(self.img_name)
		self.addKnob(self.img_save)
		self.addKnob(self.img_delete) 
		self.addKnob(self.img_update)
		self.addKnob(self.img_textCaptured)

		initCaptureBtn("images", self, capturedImages, capturedImagesBtn)

	def showModalDialog( self ):
		result = nukescripts.PythonPanel.show(self)

	def knobChanged( self, knob ): 

		global capturedImagesBtn
		global capturedImages

		if knob.name() == "save image":

			sel = nuke.selectedNodes()
			if len(sel)==1:
				if sel[0].Class()!="Viewer":

					saveImage(self.img_name.value(), self)

					name=self.img_name.value()
					if("." in name):
						name = name.split(".")[0]

					i=len(capturedImagesBtn)

					self.capBtn = nuke.PyScript_Knob(name, name)

					if i%5==0:
						self.capBtn.setFlag(nuke.STARTLINE)

					self.addKnob(self.capBtn)
					capturedImagesBtn.append(self.capBtn)

				else:
					nuke.message("Node to capture from not allowed")
			elif len(sel)==0:
				nuke.message("Please select a node to capture from")
			elif len(sel)>1:
				nuke.message("Please select only one node")

		if knob.name() == "delete image":
			deleteImageCap(self)

		if knob.name() == "update image":

			for capBtn in capturedImagesBtn:
				self.removeKnob(capBtn)

			capturedImagesBtn = []
			capturedImages = []

			#init all saved images
			for cap in os.listdir(captureImageDir):
				if cap not in dontInclude:
					capturedImages.append(cap)

			initCaptureBtn("images", self, capturedImages, capturedImagesBtn)

		#capture
		else:
			k = "%s.png" % knob.name()
			for capImg in capturedImages:
				if k == capImg:
					loadImage(knob.name())


class captureNodePanel(nukescripts.PythonPanel):
	'''
	captureNodesPanel
	'''

	def __init__(self):


		nukescripts.PythonPanel.__init__(self, 'Toolset Manager', 'com.0hufx.Capture')
		
		initCapture("nodes")

		#create elements
		
		'''image tab'''

		self.n_textSave = nuke.Text_Knob( '', 'Save / Delete', '')
		self.n_name = nuke.String_Knob('name', 'Name :')
		self.n_save = nuke.PyScript_Knob('save nodes', 'Save')  
		self.n_textspace = nuke.Text_Knob( ' ', ' ', ' ')
		self.n_textspace.setFlag(nuke.STARTLINE)
		self.n_delete = nuke.PyScript_Knob('delete nodes', 'Delete')
		self.n_update = nuke.PyScript_Knob('update nodes', 'Update')
		self.n_textCaptured = nuke.Text_Knob( '', 'Captured ', '')
		self.n_textCaptured.setFlag(nuke.STARTLINE)
		
		#add elements
		#self.addKnob(self.n_textSave)
		self.addKnob(self.n_name)
		self.addKnob(self.n_textspace)
		self.addKnob(self.n_save)
		self.addKnob(self.n_delete) 
		self.addKnob(self.n_update)
		self.addKnob(self.n_textCaptured)

		#captured nodes
		initCaptureBtn("nodes", self, capturedNodes, capturedNodesBtn)
		
	def showModalDialog( self ):
		result = nukescripts.PythonPanel.show(self)

	def knobChanged( self, knob ): 

		#flush nodes lists
		global capturedNodesBtn
		global capturedNodes

		if knob.name() == "save nodes":

			sel = nuke.selectedNodes()
			if len(sel)>0:
				
				saveNodes(self.n_name.value(), self)

				name=self.n_name.value()
				if("." in name):
					name = name.split(".")[0]

				i=len(capturedNodesBtn)

				self.capBtn = nuke.PyScript_Knob(name, name)

				if i%5==0:
					self.capBtn.setFlag(nuke.STARTLINE)

				self.addKnob(self.capBtn)
				capturedNodesBtn.append(self.capBtn)
				capturedNodes.append("%s.nk" % self.n_name.value())
	
			elif len(sel)==0:
				nuke.message("Please select at least one node to capture")
	

		if knob.name() == "delete nodes":
			deleteNodesCap(self)			

		if knob.name() == "update nodes":
			
			for capBtn in capturedNodesBtn:
				self.removeKnob(capBtn)

			capturedNodesBtn = []
			capturedNodes = []

			#init all saved nodes
			for capN in os.listdir(captureNodesDir):
				if capN not in dontInclude:
					capturedNodes.append(capN)

			initCaptureBtn("nodes", self, capturedNodes, capturedNodesBtn)

		#capture
		else:
			k = "%s.nk" % knob.name()
			for capN in capturedNodes:
				if k == capN:
					nuke.nodePaste("{0}/{1}.nk".format(captureNodesDir,knob.name()))

def showHelp():
    '''
    goto web
    '''
    url = 'http://www.leafpictures.de/capture'
    webbrowser.open_new(url)

def show(which):
	'''
	show panel
	'''
	if which=="captureImages":
		captureImagesPanel().show()
	elif which=="captureNodes":
		captureNodePanel().show()

		
# FUNCTION TO ADD IT AS A PANEL
def addCaptureManager():
    global captureManager
    captureManager = captureNodePanel()
    return captureManager.addToPane()
