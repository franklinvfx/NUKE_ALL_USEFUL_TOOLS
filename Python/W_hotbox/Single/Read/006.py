#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create Write
#
#----------------------------------------------------------------------------------------------------------

import nukescripts

def writeFromRead():
    description = ""
    for read in nuke.selectedNodes():
        #nukescripts.clear_selection_recursive()
        read = nuke.selectedNode()
        #read.setSelected(True)
        filepath = read['file'].value()
        colorspace = read['colorspace'].value()
        dirpath = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        #if read.Class()=="Read":
            
        padding = filename.split(".")[-2]
        write = nuke.createNode("Write")
        write.setName("Write_from_" + read.name())
        write['file'].setValue( dirpath + description + "/" + filename.replace("."+padding, description+"."+padding))
        write['colorspace'].setValue(colorspace)
        write['create_directories'].setValue('true')

writeFromRead()