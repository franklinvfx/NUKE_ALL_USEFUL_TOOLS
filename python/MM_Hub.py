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



if platform.system() == "Darwin": 
    dirName = "/Network/phatt/MMP/NUKE/SHARE_SCRIPT/" #PathMac
    openFolder = "os.system('open \"%s\"')" % (dirName)

elif platform.system() == "Windows":
    dirName = "Y:\\MMP\\NUKE\\SHARE_SCRIPT\\"
    openFolder = "os.system('explorer \"%s\"')" % (dirName)

MMMenuName = 'MM/SHARED SCRIPT'

mm = menubar.addMenu(MMMenuName, icon="F_customnode.png")

m.addSeparator()
menubar.addCommand("MM/Shared Selected Nodes" , 'nuke.load("MM_Share"), shareNodes()', icon="F_superswap.png")
menubar.addCommand("MM/Open Folder" , openFolder, icon="F_explore.png")
# menubar.addCommand("How it works" ,"nuke.message('blablabla')")
m.addSeparator()
menubar.addCommand("MM/Reload   ", 'nuke.load("Reload"); reloadSpecific("MM", "MM_Hub")', icon="F_reload.png")


if os.path.exists(dirName):
    for filename in os.listdir(dirName):
        if filename.endswith(".nk"):
            name = filename.split(".nk")[0].replace("_", " ")
            mm.addSeparator()
            nuke.menu('Nuke').addCommand(MMMenuName + '/' + name ,"nuke.nodePaste('"+dirName+ "/" +filename+"')")
        else:
            folder = filename
            folderModified = folder.replace('_', '')
            nuke.menu('Nuke').addMenu(MMMenuName + '/' + folderModified , "F_customnode.png")
            dirNameSubfolder = dirName + folder + '\\'
            if os.path.exists(dirNameSubfolder):
                for filename in os.listdir(dirNameSubfolder):
                    if filename.endswith(".nk"):
                        name = filename.split(".nk")[0].replace("_", " ")
                        nuke.menu('Nuke').addCommand(MMMenuName + '/' + folderModified + '/' + name ,"nuke.nodePaste('"+ dirNameSubfolder + filename +"')")

dis = nuke.menu( 'Nuke' ).addCommand( 'MM/SHARED SCRIPT/Disable' )
dis.setVisible( False )


#------------------------------------------------------------------------------------------

print '- Machine Molle Hub ............. OK'
##############################           #