#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Center pivot
#
#----------------------------------------------------------------------------------------------------------

import nuke


def center(nodes):
    def iterateCoordinate(start=None, stop=None, points=None):
        # iterating coordinates and adding them together
        axisList = []
        for i in range(start, stop, 3):
            axisList.append(points[i])
        return axisList

    for node in nodes:
        # create hidden PythonGeo node
        pyg = nuke.nodes.PythonGeo()
        pyg.setInput(0, node)

        # get geometry data of PythonGeo's input
        gObj = pyg['geo'].getGeometry()[0]

        # get tuple of all vertices of the geometry
        points = gObj.points()

        x_list = y_list = z_list = []

        # iterating over x,y and z
        x_list = iterateCoordinate(0, len(points)-2, points)
        y_list = iterateCoordinate(1, len(points)-1, points)
        z_list = iterateCoordinate(2, len(points), points)

        # calculate centred pivot coordinates
        pivot_x = (min(x_list) + max(x_list))/2
        pivot_y = (min(y_list) + max(y_list))/2
        pivot_z = (min(z_list) + max(z_list))/2

        # set geometries pivot to calculated coordinates
        node['pivot'].setValue(pivot_x, 0)
        node['pivot'].setValue(pivot_y, 1)
        node['pivot'].setValue(pivot_z, 2)

        # delete PythonGeo node after it isn't needed any more
        nuke.delete(pyg)

center(nodes=nuke.selectedNodes())
