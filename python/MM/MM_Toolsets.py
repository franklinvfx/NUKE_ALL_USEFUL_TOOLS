import nuke, nukescripts, sys, os, platform
from menu_pipe import pipe_path


# TOOLSET ADD MENU -----------------------------------------------------------------

mmtoolsets = nuke.menu("Nuke").addMenu('MM Toolsets', "MM.png")    # Dossier 

if platform.system() == "Darwin": 
    dirName = "/Network/phatt/MMP/NUKE/SHARE_SCRIPT/" #PathMac
    openFolder = "os.system('open \"%s\"')" % (dirName)

elif platform.system() == "Windows":
    dirName = "Y:\\MMP\\NUKE\\SHARE_SCRIPT\\"
    openFolder = "os.system('explorer \"%s\"')" % (dirName)


toolsetMenuName = 'MM Toolsets'


sharing_menu = nuke.menu("Nuke").addMenu(toolsetMenuName + "/SHARED SCRIPT", icon="F_deeptopos.png")
mmtoolsets.addSeparator()
nuke.menu("Nuke").addCommand(toolsetMenuName + "/Share Selected Nodes" , 'nuke.load("Share"), shareNodes()', icon="F_superswap.png")
mmtoolsets.addSeparator()
nuke.menu("Nuke").addCommand(toolsetMenuName + "/Open Folder" , openFolder, icon="F_explore.png")
dirNameModified = dirName.replace("\\", "  ")
dirpath = nuke.menu("Nuke").addCommand(toolsetMenuName + "/" + "Path (" + dirNameModified + ")", '')
dirpath.setEnabled( False )
mmtoolsets.addSeparator()
nuke.menu("Nuke").addCommand(toolsetMenuName + "/Reload   ", 'nuke.load("Reload"); reloadSpecific("MM Toolsets", "MM_Toolsets")', icon="F_reload.png")



if os.path.exists(dirName):
    for filename in os.listdir(dirName):
        if not filename.endswith(".nk") and not filename.endswith(".gizmo"):
            folder = filename
            nuke.menu('Nuke').addMenu(toolsetMenuName + "/SHARED SCRIPT" + '/' + folder , "F_customnode.png")
            sharing_menu.addSeparator()
            dirNameSubfolder = dirName + folder + '\\'
            if os.path.exists(dirNameSubfolder):
                for filename in os.listdir(dirNameSubfolder):
                    if filename.endswith(".nk") or filename.endswith(".gizmo"):
                        name = filename.split(".nk")[0]
                        name = name.split(".gizmo")[0]
                        filePath =  dirName + folder + '\\' + filename
                        nuke.menu('Nuke').addCommand(toolsetMenuName + "/SHARED SCRIPT" + '/' + folder + '/' + name ,"nuke.nodePaste('"+dirName + folder + "\\" + filename+"')")

        else:
            name = filename.split(".nk")[0].replace("_", " ")
            name = name.split(".gizmo")[0].replace("_", " ")
            nuke.menu('Nuke').addCommand(toolsetMenuName + "/SHARED SCRIPT" + '/' + name ,"nuke.nodePaste('"+dirName+ "/" +filename+"')")

 
# dis = nuke.menu( 'Nuke' ).addCommand( 'Franklin/SHARED SCRIPT/Disable' )
# dis.setVisible( False )


print '- Machine Molle Toolsets ........ OK'
##############################          #