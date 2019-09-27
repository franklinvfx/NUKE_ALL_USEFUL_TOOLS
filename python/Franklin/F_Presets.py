import nuke


#############################################################
# NODE DEFAULT VALUE
#############################################################
nuke.knobDefault('Multiply.value', '0' )
nuke.knobDefault('FilterErode.channels', 'rgba' )
nuke.knobDefault("Transform.shutteroffset", "center")
nuke.knobDefault("Tracker3.shutteroffset", "center")
nuke.knobDefault("Tracker4.shutteroffset", "center")
nuke.knobDefault("CornerPin2D.shutteroffset", "center")
nuke.knobDefault("ScanlineRender.shutteroffset", "center")
nuke.knobDefault("Project3D.crop", "false")
nuke.knobDefault("Roto.cliptype", "no clip")
nuke.knobDefault("RotoPaint.cliptype", "no clip")
nuke.knobDefault("Log2Lin.operation", "lin2log")
nuke.knobDefault("PLogLin.operation", "lin to log")
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )",  'FrameHold.png')
nuke.knobDefault("Merge.bbox", "3")
nuke.knobDefault("Keymix.bbox", "1")
nuke.knobDefault("EXPTool.mode", "0")
nuke.knobDefault("StickyNote.note_font_size", "40") 
nuke.knobDefault('BackdropNode.note_font_size', '40')
nuke.knobDefault("BackdropNode.note_font", "bold")
#nuke.knobDefault("Read.before", "3")
#nuke.knobDefault("Read.after", "3")
#nuke.knobDefault("Read.on_error", "1")
nuke.knobDefault("Write.beforeRender", "import nuke, os\nnuke.scriptSave()\n\nsrc = nuke.root().knob('name').value()\nfileName = src.split('/')[-1]\nfilePath = nuke.thisNode().knob('file').value()\nseqName = filePath.split('/')[-1]\ndst = filePath.replace(seqName ,'')\nfileDirectory = dst + fileName\n\ntry:\n    os.remove(fileDirectory)\nexcept:\n    pass\n\nfrom shutil import copy\ncopy(src, dst)\n\nfrom datetime import datetime\nnow = datetime.now()\n\ndate_time = now.strftime(\"%m-%d-%Y_%H%M%S\")\nsrcNameModified = fileDirectory.replace('.nk', '_' + date_time + '.nk')\nprint fileDirectory\nprint srcNameModified\nos.rename(fileDirectory, srcNameModified)\n\nprint 'Save a backup of the current script here:'\n\nprint ' - ' + srcNameModified")
nuke.knobDefault("Write.create_directories", "True")

#############################################################
# PRINT IN NODE LABEL
#############################################################
nuke.knobDefault("TimeOffset.label", "[value time_offset]")
nuke.knobDefault("Tracker4.label", "[value transform] / [value reference_frame]")
nuke.knobDefault("Tracker3.label", "[value transform] / [value reference_frame]")



FT = '- Franklin Presets .............. OK\n'
nuke.tprint(FT)
##############################           #