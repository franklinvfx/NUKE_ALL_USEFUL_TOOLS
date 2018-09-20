import nuke, nukescripts, math

from menu import pipe_path


def reloadMenu():
    #tell nuke to import stuff
    import os
    import menu
    #import F_Tools
    import platform

    #delete the menu.pyc file if it exits
    if os.path.isfile(pipe_path):
        os.remove(pipe_path)

    #reload the menu.py file
    reload(menu)
    from menu import *

    #delete the just created menu.pyc file
    if os.path.isfile(pipe_path):
        os.remove(pipe_path)

    nuke.message('Every menu has been reloaded')