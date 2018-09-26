﻿# Telechargé depuis https://github.com/franklinvfx/NUKE_PIPE

# Deplacez a l'endroit souhaité (en local ou sur votre réseau) le dossier et l'ensemble de son contenu.
# Copiez l'integralité de ce fichier dans votre menu.py
# Au premier lancement de nuke vous devrez selectionner le repertoire "NUKE_PIPE"
# Par la suite ce répertoire sera systématiquement mémorisé

# Copyright (c) 2018 Franklin's VFX Co.



#-----------------------------------------------------------------------------------------------------------------
# IMPORT NUKE PIPE
#-----------------------------------------------------------------------------------------------------------------
import nuke, sys, platform, os

def isPathValid(path):
    if os.path.isfile(path + "Copyright.py"):
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
    pipe_path = nuke.getFilename('Selectionner le dossier télechargé depuis Github.', '*/')

    if isPathValid(pipe_path):
        menu_file = open(nukeFolder + 'menu.py', 'r')
        menu_content = menu_file.read()
        menu_file.close()

        if platform.system() == "Darwin": 
            menu_content = menu_content.replace("'' #PathMac", "'" + pipe_path + "' #PathMac")
        elif platform.system() == "Windows": 
            menu_content = menu_content.replace("'' #PathWin", "'" + pipe_path + "' #PathWin")

        menu_file = open(nukeFolder + 'menu.py', 'w')
        menu_file.write(menu_content)
        menu_file.close()
        keepLooping = False
    else:
        nuke.message('Le dossier selectionné ne contient pas les fichiers attendu.\nFaites un autre choix.')

    print pipe_path


#-----------------------------------------------------------------------------------------------------------------
# ADD PATH
#-----------------------------------------------------------------------------------------------------------------
if isPathValid(pipe_path):
    nuke.pluginAddPath(pipe_path)

    # import MM_Config
    # import MM_Config_F
    import Home_Config
    # import LISAA_Config
    

#-----------------------------------------------------------------------------------------------------------------
# DEBUG OPTIONS
#-----------------------------------------------------------------------------------------------------------------
# import callbacksTrace                 # show all callbacks