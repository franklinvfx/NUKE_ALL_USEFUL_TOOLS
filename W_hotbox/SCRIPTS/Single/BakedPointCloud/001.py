#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Convert To PtcGenerator
#
#----------------------------------------------------------------------------------------------------------

import os
from menu import path

name = nuke.selectedNode().knob('label').value()
f = None
eltToPop = []
archive = []

path = path + '//tmp/paste.nk'
nuke.nodeCopy(path)
with open(path, 'r') as ptc_file:
    f = ptc_file.read()

f = f.split('\n')

for line in f:
    if 'serializePoints' in line or 'serializeNormals' in line or 'serializeColors' in line:
        index = f.index(line)
        f[index] = f[index].replace('"', '')

        if 'serializePoints' in line:
            f[index] = f[index].replace('serializePoints ', '')
        elif 'serializeNormals' in line:
            f[index] = f[index].replace('serializeNormals ', '')
        else:
            f[index] = f[index].replace('serializeColors ', '')
    else:
        eltToPop.append(f.index(line))

for elt in sorted(eltToPop, reverse=True):
    f.pop(elt)


posList = f[0].split(' ')
normList = f[1].split(' ')
colList = f[2].split(' ')

try:
    numPoints = long(posList[0])
except:
    posList.pop(0)
    numPoints = long(posList[0])
posList.pop(0)
normList.pop(0)
colList.pop(0)

for i in range (0, numPoints-1):
    archive.append(posList[3*i])
    archive.append(posList[3*i + 1])
    archive.append(posList[3*i + 2])
    archive.append(normList[3*i])
    archive.append(normList[3*i + 1])
    archive.append(normList[3*i + 2])
    archive.append(colList[3*i])
    archive.append(colList[3*i + 1])
    archive.append(colList[3*i + 2])
    archive.append('0 0 9 16 0')

ptcGenNode = 'PointCloudGenerator {\n inputs 0\n'
ptcGenNode += ' serializeKnob "22 serialization::archive 9 0 0 0 0 %s 1 0 1 %s"\n' % (numPoints, ' '.join(archive))
ptcGenNode += ' pointSize 0.5\n'
ptcGenNode += ' name PointCloudGen\n'
ptcGenNode += ' label Generator\n}\n'

ptcOutput = 'Output {\n'
ptcOutput += ' name Output1\n'
ptcOutput +=  'xpos -87\n'
ptcOutput += ' ypos 79\n}\n'
ptcOutput += 'end_group'

ptcGroup = '''Group {
inputs 0
name PointCloud_Edit
tile_color 0xffffffff
addUserKnob {20 User l "PointCloud - Edit"}
addUserKnob {41 point_size l "     Point Size" T PointCloudGen.pointSize}
addUserKnob {26 S10 l " " T " "}
addUserKnob {26 S01 l " "}
addUserKnob {41 displayGroups l "Display groups in overlay" T PointCloudGen.displayGroups}
addUserKnob {41 outputGroups l "Output visible groups only" T PointCloudGen.outputGroups}
addUserKnob {26 S00 l " " T " "}
addUserKnob {41 createGroup l "Create Group" T PointCloudGen.createGroup}
addUserKnob {41 deleteGroup l "Delete Selected Groups" -STARTLINE T PointCloudGen.deleteGroup}
addUserKnob {26 S02 l " " T " "}
addUserKnob {41 groups l "" -STARTLINE T PointCloudGen.groups}
addUserKnob {26 S03 l " " T " "}
addUserKnob {22 bakeGroups l "Bake Selected Groups" -STARTLINE T "
if nuke.thisKnob().name() == 'bakeGroups':
    with nuke.thisNode():
        for node in nuke.allNodes():
            if node.Class() == 'PointCloudGenerator':
                node.selectOnly()
                node.setSelected(False)
                node.showControlPanel()
                node.knob('bakeGroups').execute()
                node.hideControlPanel()
                nuke.nodeCopy(nukescripts.cut_paste_file())
                nuke.delete(nuke.selectedNode())
    t = nuke.nodePaste(nukescripts.cut_paste_file())
    t.setXpos(t.xpos()+150)
"}
addUserKnob {22 bakeMesh l "Bake Selected Groups to Mesh" -STARTLINE T "
if nuke.thisKnob().name() == 'bakeMesh':
    with nuke.thisNode():
        for node in nuke.allNodes():
            if node.Class() == 'PointCloudGenerator':
                node.selectOnly()
                node.setSelected(False)
                node.showControlPanel()
                node.knob('bakeMesh').execute()
                node.hideControlPanel()
                nuke.nodeCopy(nukescripts.cut_paste_file())
                nuke.delete(nuke.selectedNode())
    t = nuke.nodePaste(nukescripts.cut_paste_file())
    t.setXpos(t.xpos()+150)
"}
addUserKnob {26 S04 l " "}
addUserKnob {41 samplesPerNode l Samples T PointCloudGen.samplesPerNode}
addUserKnob {26 by1 l " " T " \n"}
addUserKnob {26 by2 l " " T "                                                                                               "}
addUserKnob {26 CGEV l " " t "\nEn cas de probleme, contacter Gaetan Baldy sur le chat\n" -STARTLINE T "<font color='#1C1C1C'> v01 - CGEV - 2016"}
addUserKnob {1 output l INVISIBLE +INVISIBLE}
output %s
}
''' % (name)

with open(path, 'w') as ptc_file:
    ptc_file.write(ptcGroup + ptcGenNode + ptcOutput)

nuke.nodePaste(path)
os.remove(path)