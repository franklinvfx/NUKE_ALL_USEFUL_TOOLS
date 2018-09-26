#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Explorer
#
#----------------------------------------------------------------------------------------------------------

def Revealexplr():
    a=nuke.selectedNode()
    b=a['file'].value()
    u=os.path.split(b)[0]
    u = os.path.normpath(u)
    cmd = 'explorer "%s"' % (u)
    os.system(cmd)
    
Revealexplr()