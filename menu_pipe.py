'''
https://github.com/franklinvfx/NUKE_TOOLS

1. Deplacer le dossier "NUKE_TOOLS" et l'ensemble de son contenu a l'endroit souhaite (en local ou sur votre reseau).
2. Deplacer ce fichier dans ton repertoire .nuke local (exemple: C:/Users/Franklin/.nuke)
2. Copier / coller les 3 lignes suivantes n'importe ou dans ton fichier menu.py

#>>>F_Start
import menu_pipe
#>>>F_End

3. Au premier lancement de nuke, selectionnez l'emplacement du repertoire "NUKE_TOOLS"
   Par la suite ce repertoire sera systematiquement memorise.


Copyright (c) 2018 Franklin VFX Co.
'''

#-----------------------------------------------------------------------------------------------------------------
# SET FOLDER FOR NUKE TOOLS
#-----------------------------------------------------------------------------------------------------------------
import nuke, sys, platform, os

def isPathValid(path):
    if os.path.isfile(path + "Authors.py"):
        return True
    else:
        return False

if platform.system() == "Darwin": 
    pipe_path = '' #PathMac

elif platform.system() == "Windows":
    pipe_path = '' #PathWin

nukeFolder = os.path.expanduser('~') + '/.nuke/'
keepLooping = not isPathValid(pipe_path)

while keepLooping and (pipe_path == "[EMPTY_PATH]" or pipe_path == "" or not isPathValid(pipe_path)):
    pipe_path = nuke.getFilename('Selectionner le dossier telecharge depuis https://github.com/franklinvfx/NUKE_TOOLS', '*/')

    if isPathValid(pipe_path):
        menu_file = open(nukeFolder + 'menu_pipe.py', 'r')
        menu_content = menu_file.read()
        menu_file.close()

        if platform.system() == "Darwin": 
            menu_content = menu_content.replace("'' #PathMac", "'" + pipe_path + "' #PathMac")
        elif platform.system() == "Windows": 
            menu_content = menu_content.replace("'' #PathWin", "'" + pipe_path + "' #PathWin")

        menu_file = open(nukeFolder + 'menu_pipe.py', 'w')
        menu_file.write(menu_content)
        menu_file.close()
        keepLooping = False
    else:
        nuke.message('Le dossier selectionne ne contient pas les fichiers attendu.\nFaites un autre choix.')


#-----------------------------------------------------------------------------------------------------------------
# ADD PATH - IMPORT CONFIG
#-----------------------------------------------------------------------------------------------------------------
if isPathValid(pipe_path):
    nuke.pluginAddPath(pipe_path + "./config")

    # import MM_Config
    # import MM_Config_F
    # import Home_Config
    import Default_Config
    

#-----------------------------------------------------------------------------------------------------------------
# DEBUG OPTIONS
#-----------------------------------------------------------------------------------------------------------------
# import callbacksTrace                 # show all callbacks