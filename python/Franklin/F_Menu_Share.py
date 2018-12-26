import nuke, nukescripts, sys, os, platform

from menu_pipe import pipe_path


# MACHINE MOLLE PROD MENU -----------------------------------------------------------------

nuke.menu("Nuke").addMenu('F Toolsets', "F_customnode.png")    # Dossier 

if platform.system() == "Darwin": 
    dirName = "" #PathMac
    openFolder = "os.system('open \"%s\"')" % (dirName)

elif platform.system() == "Windows":
    dirName = "D:\\WORK\\SHARING_SCRIPTS\\"
    openFolder = "os.system('explorer \"%s\"')" % (dirName)


print dirName

MMMenuName = 'F Toolsets/SHARED SCRIPT'

mm = nuke.menu("Nuke").addMenu(MMMenuName, icon="F_customnode.png")

# m.addSeparator()
nuke.menu("Nuke").addCommand("F Toolsets/Shared Selected Nodes" , 'nuke.load("F_Share"), shareNodes()', icon="F_superswap.png")
nuke.menu("Nuke").addCommand("F Toolsets/Open Folder" , openFolder, icon="F_explore.png")
# menubar.addCommand("How it works" ,"nuke.message('blablabla')")
# m.addSeparator()
nuke.menu("Nuke").addCommand("F Toolsets/Reload   ", 'nuke.load("Reload"); reloadSpecific("F Toolsets", "F_Menu_Share")', icon="F_reload.png")


if os.path.exists(dirName):
    for filename in os.listdir(dirName):
        if filename.endswith(".nk"):
            name = filename.split(".nk")[0].replace("_", " ")
            mm.addSeparator()
            nuke.menu('Nuke').addCommand(MMMenuName + '/' + name ,"nuke.nodePaste('"+dirName+ "/" +filename+"')")
        else:
            folder = filename
            folderModified = folder.replace('', '')
            nuke.menu('Nuke').addMenu(MMMenuName + '/' + folderModified , "F_customnode.png")
            dirNameSubfolder = dirName + folder + '\\'
            if os.path.exists(dirNameSubfolder):
                for filename in os.listdir(dirNameSubfolder):
                    if filename.endswith(".nk"):
                        name = filename.split(".nk")[0].replace("", "")
                        nuke.menu('Nuke').addCommand(MMMenuName + '/' + folderModified + '/' + name ,"nuke.nodePaste('"+ dirNameSubfolder + "\\" + filename +"')")

# dis = nuke.menu( 'Nuke' ).addCommand( 'Franklin/SHARED SCRIPT/Disable' )
# dis.setVisible( False )


#------------------------------------------------------------------------------------------

print '- F SHAAAAAARE ............. OK'
##############################           #