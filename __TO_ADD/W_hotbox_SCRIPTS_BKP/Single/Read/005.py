#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set Colorspace
#
#----------------------------------------------------------------------------------------------------------

from cgev.pipeline.data import session

if session.getContext().getProjectObject() is not None:
    projectColorSpace = session.getContext().getProjectObject().getLogColorspace()
    
    print projectColorSpace
    
    for i in nuke.selectedNodes():
        i.knob('colorspace').setValue(projectColorSpace)
else:
    nuke.message('You have to set your context before you can do this')