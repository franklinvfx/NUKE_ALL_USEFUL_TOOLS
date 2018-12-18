import nuke, nukescripts, math, os
import importlib
import sys

# import MM_Hub
# import F_Hub

from menu_pipe import pipe_path

def deletePycFromFolder(fpath):
    listfiles = os.listdir(fpath)
    for f in listfiles:
        if os.path.isfile(fpath + f) and f.endswith(".pyc"):
            try:
                os.remove(fpath + f)
            except:
                print 'WARNING: file reload ignored for ' + f


def reloadSpecific(menuToReload, moduleToReload):
    folderPath = os.path.expanduser('~') + '/.nuke/'

    deletePycFromFolder(folderPath)
    deletePycFromFolder(pipe_path)

    importlib.import_module(moduleToReload)###
    m = nuke.menu("Nuke").findItem(menuToReload)
    m.clearMenu()
    reload(sys.modules[moduleToReload])
    importlib.import_module(moduleToReload)

    print moduleToReload + " has been reloaded!"
