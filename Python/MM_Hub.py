import nuke, nukescripts, sys, os, platform

from menu import pipe_path

# MACHINE MOLLE PROD MENU -----------------------------------------------------------------

menubar = nuke.menu("Nuke")
m = menubar.addMenu("MM", icon="MM.png")

#------------------------------------------------------------------------------------------

m.addMenu("SEPHORA")
noth = m.addCommand("SEPHORA/Nothing", "nuke.nodePaste(path + 'SEPHORA/no.nk')")
noth.setEnabled(False)
#m.addCommand("SEPHORA/Grain", "nuke.nodePaste(Tool_path + 'SEPHORA/Grain.nk')")

#------------------------------------------------------------------------------------------


dirName = "Y:\\MMP\\NUKE\\SHARE_SCRIPT\\"
mmTemplatesMenuName = 'MM/SHARE SCRIPT/'
menubar.addCommand(mmTemplatesMenuName + "HOW IT WORKS" ,"nuke.message('Heu')")
#menubar.addCommand(mmTemplatesMenuName + "OPEN FOLDER" ,"Explr()")

def Explr():
    b = mmTemplatesMenuName
    u = os.path.split(b)[0]
    u = os.path.normpath(u)
    cmd = 'explorer "%s"' % (u)
    os.system(cmd)

if os.path.exists(dirName):
    for filename in os.listdir(dirName):
        if filename.endswith(".nk"):
            name = filename.split(".nk")[0].replace("_", " ")
            nuke.menu('Nuke').addCommand(mmTemplatesMenuName + name ,"nuke.nodePaste('"+dirName+ "/" +filename+"')")


#------------------------------------------------------------------------------------------

m.addSeparator()
m.addCommand("Reload   ", "Reload.reloadMenu()", icon="MM.png")




print '- Machine Molle Hub ............. OK'
##############################           #