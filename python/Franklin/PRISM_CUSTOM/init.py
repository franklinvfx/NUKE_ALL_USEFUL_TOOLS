#>>>> A cCopier to init.py ou menu.py

#>>> Add Option to Prism menu
import setRelPath
toolbar = nuke.toolbar("Nodes")
nuke.toolbar("Nodes").addMenu("Image").addSeparator()
toolbar.addCommand( "Image/Write_Prism", "nuke.createNode(\"WritePrism\")", 'w', icon = 'F_write.png')

prismSlashMenu = nuke.menu('Nuke').addCommand( 'Prism/--------------------------------------------------')
prismSlashMenu.setEnabled( False )
nuke.menu('Nuke').addCommand('Prism/Options/Set Relative Path',setRelPath.setPath)
#<<<