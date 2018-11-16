"""dev/ release operating system switch for main module."""

# Import built-in modules
import os
import sys


# development => py files
if os.path.isfile(os.path.join(os.path.dirname(__file__), ".dev")):
    from smartScripter_d import *
    print "smartScripter | dev | ", sys.platform

# release => cython files
else:
    print "cragl loading: smartScripter"

    if sys.platform == 'darwin':
        from smartScripter_m import *
    elif sys.platform == 'linux2':
        from smartScripter_l import *
    elif sys.platform == 'win32' or sys.platform == 'windows':
        from smartScripter_w import *
