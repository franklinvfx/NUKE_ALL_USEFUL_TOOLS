import nuke, nukescripts, sys, os, platform

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


dirName = "Y:\\MMP\\NUKE\\SHARE_SCRIPT\\"
MMMenuName = 'MM/SHARE SCRIPT/'

m = menubar.addMenu("MM/SHARE SCRIPT", icon="MM.png")
menubar.addCommand(MMMenuName + "HOW IT WORKS" ,"nuke.message('Heu')")
menubar.addCommand(MMMenuName + "OPEN SHARED FOLDER" , "os.system('explorer \"%s\"')" % (dirName))
m.addSeparator()

if os.path.exists(dirName):
    for filename in os.listdir(dirName):
        if filename.endswith(".nk"):
            name = filename.split(".nk")[0].replace("_", " ")
            
            nuke.menu('Nuke').addCommand(MMMenuName + name ,"nuke.nodePaste('"+dirName+ "/" +filename+"')")


#------------------------------------------------------------------------------------------

m.addSeparator()
m.addCommand("Reload   ", 'nuke.load("Reload"); reloadSpecific("MM", "MM_Hub")', icon="MM.png")


print '- Machine Molle Hub ............. OK'
##############################           #