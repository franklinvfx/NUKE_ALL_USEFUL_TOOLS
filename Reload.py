import nuke, nukescripts, math

from menu import path


def reloadMenu():
    #tell nuke to import stuff
    import os
    import menu
    import F_Tools
    import platform

    #delete the menu.pyc file if it exits
    if os.path.isfile(path):
        os.remove(path)

    #reload the menu.py file
    reload(F_Tools)
    from F_Tools import *

    #delete the just created menu.pyc file
    if os.path.isfile(path):
        os.remove(path)

    nuke.message('Every menu has been reloaded')