import nuke, nukescripts, sys, os, os.path, platform
from MM_Toolsets import dirName


def shareNodes():
    print dirName
    folder = next(os.walk(dirName))[1]
    folder =  " ".join(folder)
    folder = folder.replace('Disable', '')
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

        fullName = p.value("Node Name Setup:")
        fileName = fullName.split("/")[-1]
        fileNameChanged = "_" + fileName
        newFolder = fullName.split("/")[0]

        if p.value('Project') == 'Root':
            if fileName == newFolder:
                nukeFile = dirName + fileNameChanged + '.nk'
            else:
                subDir = dirName + newFolder
                os.mkdir(subDir)
                nukeFile = subDir + "\\" + fileNameChanged + '.nk'
        else:
            folderChoose = p.value('Project')
            nukeFile = dirName + folderChoose + "\\" + fileNameChanged + '.nk'

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

                nuke.load("Reload"); reloadSpecific("F Toolsets", "MM_Toolsets")
    else:
        return