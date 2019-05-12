import nuke
import PrismCore
pcore = PrismCore.PrismCore(app="Nuke")

def setPath():
	tmpWrite = nuke.createNode('WritePrism')
	tmpWrite.hideControlPanel()
	tmpWrite.knob('name').setValue('tmp_WP')
	fullPath = pcore.appPlugin.getOutputPath(nuke.toNode('tmp_WP').node("WritePrismBase"), nuke.selectedNode())
	#print fullPath

	relPath = fullPath.split('01_Workflow')[0]
	nuke.root()['project_directory'].setValue(relPath)

	for i in nuke.allNodes():
	    nodeClass = i.Class() 
	    if nodeClass == 'Read':
	        i.knob('selected').setValue(True)
	        filename = i.knob('file').value()
	        oldPath = filename.split('01_Workflow')[0]
	        filename = filename.replace(oldPath,'./')
	        i.knob('file').setValue(filename)

	print "Project path is: \n" + relPath + "\n\nPath changed to relative."

	nuke.delete(tmpWrite)
	nuke.selectAll() 
	nuke.invertSelection()