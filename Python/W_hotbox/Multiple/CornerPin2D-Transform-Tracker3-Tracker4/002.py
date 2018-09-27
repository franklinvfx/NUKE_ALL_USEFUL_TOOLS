#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Merge Transforms
#
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Merge Transforms
#
#----------------------------------------------------------------------------------------------------------

def main():
    '''
    www.erwanleroy.com
    To install: 
    Place file in a directory that is part of the Nuke Plugin Path.
    In a menu.py add 'import merge_transforms_v2'
    In a menu of your choice, create a command 'merge_transforms_v2.start()'
    '''
    
    import math
    import nuke
    import nukescripts
    import threading
    
    # Matrix to CornerPin rarely fails
    
    
    def sort_nodes(node_list):
        # Sorts selected nodes by number of parents of an allowed class
        nodes_in_list = 0
        sorted_list = []
        for n in node_list:
            has_parents = True
            number_of_nodes = 1
            list_of_nodes = [n]
            # we count how many parents the node has
            while has_parents:
                p = n.input(0)
                if p:
                    if p['selected'].value():
                        n = p
                        number_of_nodes += 1
                        list_of_nodes.append(n)
                    else:
                        has_parents = False
                else:
                    has_parents = False
    
                    # the node with the biggest number of parents is our last node
            if number_of_nodes > nodes_in_list:
                nodes_in_list = number_of_nodes
                sorted_list = list_of_nodes
    
        # We want our first node first though, so we reverse the list
        sorted_list.reverse()
        return sorted_list
    
    
    def print_matrix4(m):
        row = '| ' + 4 * '{: .4f} ' + '|'
        print row.format(m[0], m[4], m[8], m[12])
        print row.format(m[1], m[5], m[9], m[13])
        print row.format(m[2], m[6], m[10], m[14])
        print row.format(m[3], m[7], m[11], m[15])
    
    
    def decompose_matrix(m, center_x=0, center_y=0):
        # Solve Translation
        vector = nuke.math.Vector3(center_x, center_y, 0)
        vector_trans = m.transform(vector)
        translate_x = vector_trans[0] - center_x
        translate_y = vector_trans[1] - center_y
        # Solve Rotation/Scale/Skew
        # Skew Y is never solved, will be reflected in Rotation instead.
        delta = (m[0] * m[5]) - (m[4] * m[1])
        r = pow(m[0], 2) + pow(m[1], 2)
        rotation = math.degrees(math.atan2(m[1], m[0]))
        scale_x = math.sqrt(r)
        scale_y = delta / scale_x
        skew_x = (m[0] * m[4] + m[1] * m[5]) / delta
        return translate_x, translate_y, rotation, scale_x, scale_y, skew_x
    
    
    def matrix_to_cornerpin(matrix, cornerpin_node, frame, width, height):
        v1 = nuke.math.Vector4(0, 0, 0, 1)
        v1 = matrix.transform(v1)
        v1 /= v1.w
        v2 = nuke.math.Vector4(width, 0, 0, 1)
        v2 = matrix.transform(v2)
        v2 /= v2.w
        v3 = nuke.math.Vector4(width, height, 0, 1)
        v3 = matrix.transform(v3)
        v3 /= v3.w
        v4 = nuke.math.Vector4(0, height, 0, 1)
        v4 = matrix.transform(v4)
        v4 /= v4.w
        for i in xrange(2):
            cornerpin_node['to1'].setValueAt(v1[i], frame, i)
            cornerpin_node['to2'].setValueAt(v2[i], frame, i)
            cornerpin_node['to3'].setValueAt(v3[i], frame, i)
            cornerpin_node['to4'].setValueAt(v4[i], frame, i)
        return
    
    
    def get_matrix_at_frame(node, frame):
        matrix = None
        if node.Class() == 'Transform' or node.Class() == 'Tracker4':
            k = node.knob('matrix')
            context = nuke.OutputContext()
            context.setFrame(frame)
            matrix = k.value(context)
        elif node.Class() == 'CornerPin2D':
            # Calculate 'to' matrix
            to_matrix = nuke.math.Matrix4()
            to1x = node['to1'].getValueAt(frame)[0]
            to1y = node['to1'].getValueAt(frame)[1]
            to2x = node['to2'].getValueAt(frame)[0]
            to2y = node['to2'].getValueAt(frame)[1]
            to3x = node['to3'].getValueAt(frame)[0]
            to3y = node['to3'].getValueAt(frame)[1]
            to4x = node['to4'].getValueAt(frame)[0]
            to4y = node['to4'].getValueAt(frame)[1]
            to_matrix.mapUnitSquareToQuad(to1x, to1y, to2x, to2y, to3x, to3y, to4x, to4y)
            # Calculate 'to' matrix
            from_matrix = nuke.math.Matrix4()
            from1x = node['from1'].getValueAt(frame)[0]
            from1y = node['from1'].getValueAt(frame)[1]
            from2x = node['from2'].getValueAt(frame)[0]
            from2y = node['from2'].getValueAt(frame)[1]
            from3x = node['from3'].getValueAt(frame)[0]
            from3y = node['from3'].getValueAt(frame)[1]
            from4x = node['from4'].getValueAt(frame)[0]
            from4y = node['from4'].getValueAt(frame)[1]
            from_matrix.mapUnitSquareToQuad(from1x, from1y, from2x, from2y, from3x, from3y, from4x, from4y)
            # Calculate the extra matrix
            k = node.knob('transform_matrix')
            values = k.getValueAt(frame)
            extra_matrix = nuke.math.Matrix4()
            for i in xrange(len(values)):
                extra_matrix[i] = values[i]
            extra_matrix.transpose()
    
            matrix = extra_matrix * (to_matrix * from_matrix.inverse())
    
            if node['invert'].getValueAt(frame):
                matrix = matrix.inverse()
    
        return matrix
    
    
    def check_classes(nodes, allowed_classes):
        valid = True
        for n in nodes:
            if n.Class() not in allowed_classes:
                nuke.message("Please select only supported Nodes:"+', '.join(allowed_classes))
                valid = False
                break
        return valid
    
    
    def fuse_transforms(transform_list, first, last, cornerpin=False, force_matrix=False):
        # Set Threading
        task = nuke.ProgressTask("Merging Transforms")
        task.setMessage("Checking Settings")
        # Check if we only have Cornerpins in the list
        for n in transform_list:
            if n.Class() == 'CornerPin2D':
                cornerpin = True
    
        # Our nodes resolution might be useful too
        height = transform_list[0].height()
        width = transform_list[0].width()
    
        # Create the node to receive the baked transformations
        if cornerpin:
            new_node = nuke.nodes.CornerPin2D(inputs=[transform_list[0].input(0)],
                                              xpos=transform_list[0]['xpos'].value() + 100,
                                              ypos=transform_list[0]['ypos'].value(),
                                              label='Merged Transform')
            new_node['from1'].setValue(0, 0)
            new_node['from1'].setValue(0, 1)
            new_node['from2'].setValue(width, 0)
            new_node['from2'].setValue(0, 1)
            new_node['from3'].setValue(width, 0)
            new_node['from3'].setValue(height, 1)
            new_node['from4'].setValue(0, 0)
            new_node['from4'].setValue(height, 1)
            if not first == last:
                # More than one frame, enable animation
                if not force_matrix:
                    new_node['to1'].setAnimated()
                    new_node['to2'].setAnimated()
                    new_node['to3'].setAnimated()
                    new_node['to4'].setAnimated()
                else:
                    new_node['transform_matrix'].setAnimated()
        else:
            new_node = nuke.nodes.Transform(inputs=[transform_list[0].input(0)],
                                            xpos=transform_list[0]['xpos'].value() + 100,
                                            ypos=transform_list[0]['ypos'].value(),
                                            label='Merged Transform')
            new_node['center'].setValue(width/2, 0)
            new_node['center'].setValue(height/2, 1)
            if not first == last:
                # More than one frame, enable animation
                new_node['translate'].setAnimated()
                new_node['rotate'].setAnimated()
                new_node['scale'].setAnimated()
                new_node['skewX'].setAnimated()
    
        task.setMessage("Merging transforms")
    
        # We need the calculation for each frame
        try:
            for frame in xrange(first, last + 1):
                if task.isCancelled():
                    break
                current_matrix = get_matrix_at_frame(transform_list[0], frame)
                print 'Calculating Frame: {}'.format(frame)
                print_matrix4(current_matrix)
                # We merge the nodes 2 by two
                for i in range(1, len(transform_list)):
                    # Access the matrix knobs the next transformation
                    transform_matrix = get_matrix_at_frame(transform_list[i], frame)
                    print 'x'
                    print_matrix4(transform_matrix)
                    current_matrix = transform_matrix * current_matrix
                    print '='
                    print_matrix4(current_matrix)
    
                if cornerpin:
                    if force_matrix:
                        current_matrix.transpose()
                        for i in xrange(16):
                            new_node.knob('transform_matrix').setValueAt(current_matrix[i], frame, i)
                    else:
                        matrix_to_cornerpin(current_matrix, new_node, frame, width, height)
                else:
                    translate_x, translate_y, rotation, scale_x, scale_y, skew_x = decompose_matrix(current_matrix,
                                                                                                    width/2, height/2)
                    new_node['translate'].setValueAt(translate_x, frame, 0)
                    new_node['translate'].setValueAt(translate_y, frame, 1)
                    new_node['rotate'].setValueAt(rotation, frame)
                    new_node['scale'].setValueAt(scale_x, frame, 0)
                    new_node['scale'].setValueAt(scale_y, frame, 1)
                    new_node['skewX'].setValueAt(skew_x, frame)
    
                # set thread progress
                task.setProgress(int((frame - first) / ((last - first) * 0.01)))
        except:
            raise
        finally:
            task.setProgress(100)
            del task
    
    
    def start():
        nodes = nuke.selectedNodes()
        valid_nodes = check_classes(nodes, ['Transform', 'CornerPin2D', 'Tracker4'])
        if valid_nodes:
            transform_list = sort_nodes(nodes)
        else:
            return 0
    
        # We check that we have at least 2 transforms, otherwise no point in merging
        if len(transform_list) < 2:
            nuke.message("You need at least 2 transforms selected")
            return 0
        elif len(transform_list) != len(nodes):
            nuke.message("Please make sure all nodes form a single Branch")
            return 0
        p = MergeTransformsPanel()
        if p.showModalDialog():
            first = p.first.value()
            last = p.last.value()
            cornerpin = p.forceCP.value()
            force_matrix = p.forceMatrix.value()
            exec_thread = threading.Thread(None, fuse_transforms(transform_list, first, last, cornerpin, force_matrix))
            exec_thread.start()
            #exec_thread.join()
    
    
    class MergeTransformsPanel(nukescripts.PythonPanel):
        def __init__(self):
            nukescripts.PythonPanel.__init__(self, 'Merge Transforms')
    
            # CREATE KNOBS
            self.first = nuke.Int_Knob('first', 'First Frame')
            self.first.setValue(int(nuke.root()['first_frame'].value()))
            self.last = nuke.Int_Knob('last', 'Last Frame')
            self.last.setValue(int(nuke.root()['last_frame'].value()))
            self.forceCP = nuke.Boolean_Knob('force_cp', 'Force Merge as CornerPin')
            self.forceCP.setFlag(nuke.STARTLINE)
            self.forceCP.setTooltip('Tool will merge transforms a a new Transform if possible, or Cornerpin if necessary.'
                                    '\nChecking this box will force a corner pin output')
            self.forceMatrix = nuke.Boolean_Knob('force_matrix', 'CornerPin as extra_matrix')
            self.forceMatrix.setTooltip("Uses the cornerpin's extra_matrix to recreate the transform rather than the corners")
            self.forceMatrix.setEnabled(False)
            self.forceMatrix.setFlag(nuke.STARTLINE)
    
            # ADD KNOBS
            for k in (self.first, self.last, self.forceCP, self.forceMatrix):
                self.addKnob(k)
    
        def knobChanged( self, knob ):
            # ONLY SHOW FORCEMATRIX IF CORNERPIN IS ON
            if knob is self.forceCP:
                self.forceMatrix.setEnabled(self.forceCP.value())
    
    
    start()
main()