#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create Thumbnail
#
#----------------------------------------------------------------------------------------------------------

import nuke
import os

def createThumbnail():
    fileType = "jpg"
    imageSize = 0.15
    try:
        sel = nuke.selectedNode()
    except:
        nuke.message("Need to select a node!")

    scriptsPath = nuke.selectedNode().knob('file').value().split(".")[0]
    clipname = scriptsPath.split("/")[-1]
    scriptsPath = scriptsPath.split('\\' + clipname)[0]
    scriptName = nuke.selectedNode().knob('file').value().split(".dpx")[0]
    scriptName = scriptName.split("/")[-1]

    #create thumbnail dir if not exist
    thumbnailDir = scriptsPath
    if not os.path.isdir(thumbnailDir):
        os.makedirs(thumbnailDir)

    #full thumbnail path
    fullThumbnailPath = "{thumbnailDir}/{nodeName}_{frame}.{ext}".format(thumbnailDir=thumbnailDir, nodeName = clipname, frame = nuke.frame(), ext = fileType)

    #reformat node
    r = nuke.createNode("Reformat", inpanel = False)
    r.setInput(0,sel)
    r.setXYpos(sel.xpos(), sel.ypos()+50)
    r["type"].setValue("scale")
    r["scale"].setValue(imageSize)

    #write node
    w = nuke.createNode("Write", inpanel = False)
    w.setInput(0,r)
    w.setXYpos(r.xpos(), r.ypos()+50)
    w.knob("name").setValue("capture")
    w.knob("use_limit").setValue(True)
    w.knob("first").setValue(nuke.frame())
    w.knob("last").setValue(nuke.frame())
    w.knob("file_type").setValue(fileType)
    w.knob("file").setValue(fullThumbnailPath)
    nuke.execute(w,nuke.frame(),nuke.frame())

    nuke.delete(r)
    nuke.delete(w)
    
    nuke.message(clipname + " \n\nThumbnail OK")

createThumbnail()