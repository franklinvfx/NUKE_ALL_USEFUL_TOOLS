import nuke, nukescripts, sys, os, platform

# NODE DEFAULT PRESETS ---------------------------------------------------------------------

nuke.knobDefault("Root.fps", "25")

nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )",  'FrameHold.png')
nuke.knobDefault("Transform.shutteroffset", "center")
nuke.knobDefault("Tracker3.shutteroffset", "center")
nuke.knobDefault("Tracker4.shutteroffset", "center")
nuke.knobDefault("CornerPin2D.shutteroffset", "center")
nuke.knobDefault("ScanlineRender.shutteroffset", "center")

nuke.knobDefault("Write.beforeRender", "import nuke, os\nnuke.scriptSave()\n\nsrc = nuke.root().knob('name').value()\nfileName = src.split('/')[-1]\nfilePath = nuke.thisNode().knob('file').value()\nseqName = filePath.split('/')[-1]\ndst = filePath.replace(seqName ,'')\nfileDirectory = dst + fileName\n\ntry:\n    os.remove(fileDirectory)\nexcept:\n    pass\n\nfrom shutil import copy\ncopy(src, dst)\n\nfrom datetime import datetime\nnow = datetime.now()\n\ndate_time = now.strftime(\"%m-%d-%Y_%H%M%S\")\nsrcNameModified = fileDirectory.replace('.nk', '_' + date_time + '.nk')\nprint fileDirectory\nprint srcNameModified\nos.rename(fileDirectory, srcNameModified)\n\nprint 'Save a backup of the current script here:'\n\nprint ' - ' + srcNameModified")
nuke.knobDefault("Write.create_directories", "True")

'''
nuke.knobDefault("Write.colorspace", "sRGB")
nuke.knobDefault("Write.channels", "rgb")
nuke.knobDefault("Read.colorspace", "sRGB")
'''

# Read knobDefault = exr:linear / dpx:AlexaV3LogC / jpg:sRGB

# nuke.knobDefault("Read.knobChanged", "if nuke.thisKnob().name() == 'file':\n    format = nuke.thisNode().knob('file').value()\n    format = format[-3] + format[-2] + format[-1]\n    if format == 'dpx':\n        nuke.thisNode().knob('colorspace').setValue('Cineon')\n        \n    elif format == 'exr':\n        nuke.thisNode().knob('colorspace').setValue('linear')\n        \n    elif format == 'jpg':\n        nuke.thisNode().knob('colorspace').setValue('sRGB')")
# nuke.knobDefault("Read.onCreate", "format = nuke.thisNode().knob('file').value()\nformat = format[-3] + format[-2] + format[-1]\nif format == 'dpx':\n    nuke.thisNode().knob('colorspace').setValue('Cineon')\n    \nelif format == 'exr':\n    nuke.thisNode().knob('colorspace').setValue('linear')\n    \nelif format == 'jpg':\n    nuke.thisNode().knob('colorspace').setValue('sRGB')")

# Write knobDefault = exr / AlexaV3LogC / rgba

# nuke.knobDefault("Write.colorspace", "linear")

'''
nuke.knobDefault("Write.channels", "rgba")
nuke.knobDefault("Write.file_type", "exr")
nuke.knobDefault("Write.create_directories", "1")

nuke.addFormat("2880 1620 1.0 SEPH_Format")
nuke.knobDefault("Root.format", "SEPH_Format")

nuke.knobDefault("Viewer.viewerProcess", "rec709")
'''













#PRISM CUSTOM
# nuke.menu('Nodes').addCommand( 'Image/WritePrism', lambda: nuke.createNode("WritePrism"), 'w', 'Write.png')














print '- Machine Molle Presets ......... OK'
##############################           #



