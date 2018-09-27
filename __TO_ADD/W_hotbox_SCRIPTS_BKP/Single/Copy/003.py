#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Swap
#
#----------------------------------------------------------------------------------------------------------

n = nuke.selectedNode()

f0 = n['from0'].value()
t0 = n['to0'].value()
f1 = n['from1'].value()
t1 = n['to1'].value()
f2 = n['from2'].value()
t2 = n['to2'].value()
f3 = n['from3'].value()
t3 = n['to3'].value()

n['from0'].setValue(t0)
n['to0'].setValue(f0)
n['from1'].setValue(t1)
n['to1'].setValue(f1)
n['from2'].setValue(t2)
n['to2'].setValue(f2)
n['from3'].setValue(t3)
n['to3'].setValue(f3)