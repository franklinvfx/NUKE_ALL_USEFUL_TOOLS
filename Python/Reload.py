import nuke, nukescripts, math, os, menu
import MM_Hub, MM_Tools, MM_Presets
import F_Hub, F_Tools, F_Presets, F_Scripts, F_Panels
import C_Tools


from menu_pipe import pipe_path

# def deletePycFromFolder(fpath):
#     listfiles = os.listdir(fpath)
#     for f in listfiles:
#         if os.path.isfile(fpath + f) and f.endswith(".pyc"):
#             try:
#                 os.remove(fpath + f)
#             except:
#                 print 'WARNING: file reload ignored for ' + f

def reloadMenu():
    folderPath = os.path.expanduser('~') + '/.nuke/'

    # deletePycFromFolder(folderPath)
    # deletePycFromFolder(pipe_path)

    m = nuke.menu("Nuke").findItem()
    m.clearMenu()

    reload(menu)
    from menu import *



    reload(MM_Hub)
    from MM_Hub import *

    reload(MM_Tools)
    from MM_Tools import *

    reload(MM_Presets)
    from MM_Presets import *

    reload(F_Hub)
    from F_Hub import *

    reload(F_Tools)
    from F_Tools import *

    reload(F_Presets)
    from F_Presets import *

    reload(F_Scripts)
    from F_Scripts import *

    reload(F_Panels)
    from F_Panels import *

    reload(C_Tools)
    from C_Tools import *