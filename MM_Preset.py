import nuke, nukescripts, sys, os, platform

# NODE DEFAULT PRESETS ---------------------------------------------------------------------

nuke.knobDefault("Root.fps", "25")

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

'''
import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte_ui()
'''


print '- Machine Molle Presets ......... OK'
##############################           #



