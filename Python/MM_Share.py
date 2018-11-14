import nuke, nukescripts, sys, os, os.path, platform
from MM_Hub import dirName

def shareNodes():
    try:
        nuke.selectedNodes()
        nuke.nodeCopy(nukescripts.cut_paste_file())
        clipboard = QtGui.QApplication.clipboard()
        clipboard = clipboard.text()
    except:
        nuke.message("You have to select something first.")
        return

    p = nuke.Panel('Share nodes with other')
    p.addSingleLineInput('Node Name Setup:', 'Node setup')

    p.addButton('Cancel')
    p.addButton('Share')
    if p.show() == 0:
        return

    fileName = p.value("Node Name Setup:")
    nukeFile = dirName + fileName + '.nk'

    if os.path.isfile(nukeFile) == True:
        nuke.message('WARNING: File Already exist')
    else:
        menu_file = open(nukeFile, 'w+')
        print menu_file
        menu_content = menu_file.read()
        menu_file.close()
    
        menu_content = menu_content.replace("", clipboard)
    
        menu_file = open(nukeFile, 'w')
        menu_file.write(menu_content)
        menu_file.close()

        nuke.load("Reload"); reloadSpecific("MM", "MM_Hub")