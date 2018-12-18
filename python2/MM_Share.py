import nuke, nukescripts, sys, os, os.path, platform
from MM_Hub import dirName


def shareNodes():

    folder = next(os.walk(dirName))[1]
    folder =  " ".join(folder)
    folder = folder.replace('Disable', '')
    folder = folderName.replace('_', '')
    folder = 'Root ' + folder

    try:
        # < Nuke 11
        import PySide.QtGui as QtGui
        from PySide.QtGui import QApplication
    except:
        # >= Nuke 11
        import PySide2.QtWidgets as QtGui
        from PySide2.QtWidgets import QApplication

    try:
        nuke.selectedNodes()
        nuke.nodeCopy(nukescripts.cut_paste_file())
        clipboard = QtGui.QApplication.clipboard()
        clipboard = clipboard.text()
    except:
        nuke.message("You have to select something first.")
        return

    p = nuke.Panel('Share nodes with other')
    p.addEnumerationPulldown('Project', folder)
    p.addSingleLineInput('Node Name Setup:', '')

    p.addButton('Cancel')
    p.addButton('Share')

    if p.show():

        fileName = p.value("Node Name Setup:")

        newFolder = fileName.split("/")[0]
        fileName = fileName.split("/")[-1]

        if p.value('Project') == 'Root':
            if fileName == newFolder:
                nukeFile = dirName + fileName + '.nk'
            else:
                subDir = dirName + newFolder
                os.mkdir(subDir)
                nukeFile = subDir + "\\" + fileName + '.nk'
        else:
            folderChoose = '_' + p.value('Project')
            nukeFile = dirName + folderChoose + "\\" + fileName + '.nk'

        if fileName == '':
            nuke.message('WARNING: The setup need a name')
            p.show()
        else:
            if os.path.isfile(nukeFile) == True:
                nuke.message('WARNING: File Already exist')
                p.show()

            else:
                menu_file = open(nukeFile, 'w+')
                menu_content = menu_file.read()
                menu_file.close()
            
                menu_content = menu_content.replace("", clipboard)
            
                menu_file = open(nukeFile, 'w')
                menu_file.write(menu_content)
                menu_file.close()

                nuke.load("Reload"); reloadSpecific("MM", "MM_Hub")
    else:
        return