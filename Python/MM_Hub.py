import nuke, nukescripts, sys, os, platform
#import MM_Share

from menu_pipe import pipe_path


# MACHINE MOLLE PROD MENU -----------------------------------------------------------------

menubar = nuke.menu("Nuke")
m = menubar.addMenu("MM", icon="MM.png")

#------------------------------------------------------------------------------------------

# m.addMenu("SEPHORA")
# noth = m.addCommand("SEPHORA/Nothing", "nuke.nodePaste(path + 'SEPHORA/no.nk')")
# noth.setEnabled(False)
#m.addCommand("SEPHORA/Grain", "nuke.nodePaste(Tool_path + 'SEPHORA/Grain.nk')")

#------------------------------------------------------------------------------------------



if platform.system() == "Darwin": 
    dirName = "/Network/phatt/MMP/NUKE/SHARE_SCRIPT/" #PathMac
    openFolder = "os.system('open \"%s\"')" % (dirName)

elif platform.system() == "Windows":
    dirName = "Y:\\MMP\\NUKE\\SHARE_SCRIPT\\"
    openFolder = "os.system('explorer \"%s\"')" % (dirName)

MMMenuName = 'MM/SHARED SCRIPT'

mm = menubar.addMenu(MMMenuName, icon="MM.png")


#menubar.addCommand(MMMenuName + "HOW IT WORKS" ,"nuke.message('Heu')")
m.addSeparator()
menubar.addCommand("MM/Shared Selected Nodes" , 'nuke.load("MM_Share"), shareNodes()' )
# menubar.addCommand("MM/Open Shared Folder" , "os.system('explorer \"%s\"')" % (dirName))
menubar.addCommand("MM/Open Shared Folder" , openFolder)
m.addSeparator()
menubar.addCommand("MM/Reload   ", 'nuke.load("Reload"); reloadSpecific("MM", "MM_Hub")', icon="MM.png")



if os.path.exists(dirName):
    for filename in os.listdir(dirName):
        if filename.endswith(".nk"):
            name = filename.split(".nk")[0].replace("_", " ")
            
            nuke.menu('Nuke').addCommand(MMMenuName + '/' + name ,"nuke.nodePaste('"+dirName+ "/" +filename+"')")




#------------------------------------------------------------------------------------------



print '- Machine Molle Hub ............. OK'
##############################           #