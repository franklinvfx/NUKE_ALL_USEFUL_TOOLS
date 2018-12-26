import nuke
import nukescripts
import common as ch

def swapper():
    try:
        node=nuke.selectedNode()
        if node:

            nodeClass=ch.nodeClass(node)

            canHandle=['Grade','Transform','Ramp','Shuffle','CornerPin2D','Mirror','FrameHold', 'Blur', 'ColorCorrect', 'Grade']

            if nodeClass in canHandle:

                if nodeClass=='Grade':
                    node['reverse'].setValue( ((node['reverse'].getValue()+1)%2) )

                elif nodeClass=='Transform':
                    node['invert_matrix'].setValue( ((node['invert_matrix'].getValue()+1)%2) )

                elif nodeClass=='Ramp':
                    temp=node['p0'].getValue()
                    node['p0'].setValue(node['p1'].getValue())
                    node['p1'].setValue(temp)

                elif nodeClass=='Shuffle':
                    tileColor=[2369864191,1032143871,962307071,2341178367]
                    index=int(node['red'].getValue())
                    node['green'].setValue(index)
                    node['blue'].setValue(index)
                    node['alpha'].setValue(index)
                    node['tile_color'].setValue(tileColor[index-1])

                elif node.Class()=='CornerPin2D':
                    node['invert'].setValue( ((node['invert'].getValue()+1)%2) )

                elif nodeClass=='Mirror':
                    node['Horizontal'].setValue( ((node['Horizontal'].getValue()+1)%2) )
                    node['Vertical'].setValue(1-node['Horizontal'].getValue())
                    if node['Horizontal'].getValue():
                        node['label'].setValue('Horizontal')
                    else:
                        node['label'].setValue('Vertical')

                elif nodeClass=='FrameHold':
                    node['first_frame'].setValue(nuke.frame())
                elif nodeClass=='chFrameHold':
                    node['chFrame'].setValue(nuke.frame())

                elif nodeClass=='Blur':
                    if node['channels'].value()=='all':
                        node['channels'].setValue('alpha')
                    elif node['channels'].value()=='alpha':
                        node['channels'].setValue('all')
						
                elif nodeClass=='ColorCorrect':
                    if node['channels'].value()=='rgb':
                        node['channels'].setValue('all')
                    elif node['channels'].value()=='all':
                        node['channels'].setValue('rgb')
						
            else:
                 nukescripts.swapAB(node)
    except Exception, e:
        nuke.message('Error:: %s' % e)
