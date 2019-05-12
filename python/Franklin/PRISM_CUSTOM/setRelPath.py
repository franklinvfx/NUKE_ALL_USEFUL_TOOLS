import nuke

def setPath():
	tmpWrite = nuke.createNode('WritePrism')
	#tmpWrite.hideControlPanel()
	tmpWrite.knob('name').setValue('tmp_WP')
	fullPath = tmpWrite.knob("fileName").value()
	print fullPath


	relPath = fullPath.split('01_Workflow')[0]
	nuke.root()['project_directory'].setValue(relPath)

	for i in nuke.allNodes():
	    nodeClass = i.Class() 
	    if nodeClass == 'Read':
	        i.knob('selected').setValue(True)
	        filename = i.knob('file').value()
	        oldPath = filename.split('01_Workflow')[0]
	        filename = filename.replace(oldPath,'./')
	        #print 'relPath = ' + filename
	        i.knob('file').setValue(filename)
	        #changedReads = i.knob('name').value()

	nuke.message("Project path is: \n" + relPath + "\n\nPath changed to relative.")

	nuke.delete(tmpWrite)