#>>>> A Copier dans menu.py

#>>> Add Options to Prism menu
toolbar = nuke.toolbar("Nodes")
nuke.toolbar("Nodes").addMenu("Image").addSeparator()
toolbar.addCommand( "Image/Write_Prism", "nuke.createNode(\"WritePrism\")", 'w', icon = 'F_write.png')

prismSlashMenu = nuke.menu('Nuke').addCommand( 'Prism/--------------------------------------------------')
prismSlashMenu.setEnabled( False )
nuke.menu('Nuke').addCommand('Prism/Options/Set Relative Path',setRelPath.setPath)