#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: cardToTrack
#
#----------------------------------------------------------------------------------------------------------

def main():
    try:
        import nuke
    except ImportError:
        pass
    
    # =============================================================================
    # EXPORTS
    # =============================================================================
    
    __all__ = [
        'card_to_track',
        'card_to_track_wrapper',
        'corner_pin_to_corner_matrix',
        'matrix_to_roto_matrix',
        'reconcile_to_corner',
        'reconcile_to_tracks',
    ]
    
    # =============================================================================
    # PRIVATE FUNCTIONS
    # =============================================================================
    
    
    def _card_to_track_panel():
        """GUI panel for getting card_to_track settings
    
        Args:
            N/A
    
        Returns:
            {
                'frange': (str) Frame Range,
                'first': (int) First Frame,
                'last': (int) Last Frame,
                'ref_frame': (int) Reference Frame,
                'output': Output Type,
                'axis': Translate Only Bool
             }
    
        Raises:
            N/A
    
        """
        # Grab our current frame to be used as default for ref_frame
        frame = nuke.frame()
    
        panel_results = {}
    
        # And our current frange to use as the default for range
        first = int(nuke.Root()['first_frame'].value())
        last = int(nuke.Root()['last_frame'].value())
    
        # Construct our panel
        panel = nuke.Panel("Card to Track")
    
        panel.addEnumerationPulldown(
            "Output:",
            "All "
            "CornerPin "
            "CornerPin(Matrix) "
            "Roto "
            "Tracker"
        )
        panel.addSingleLineInput(
            "Range:",
            "{first}-{last}".format(
                first=first,
                last=last,
            )
        )
        panel.addSingleLineInput("Ref frame:", frame)
        panel.addBooleanCheckBox('Translate Only', False)
    
        # Show Panel
        if not panel.show():
            return
    
        # Get our entered values
        panel_results['frange'] = panel.value("Range:")
        panel_results['ref_frame'] = int(panel.value("Ref frame:"))
        panel_results['output'] = panel.value("Output:")
        panel_results['axis'] = panel.value("Translate Only")
    
        # Split returned range
        first, last = panel_results['frange'].split("-")
        panel_results['first'] = int(first)
        panel_results['last'] = int(last)
    
        return panel_results
    
    # =============================================================================
    
    
    def _create_axis(card, offset, parent_axis, name, xform=True):
        """Creates an axis along the plane of a card.
    
        Args:
            card : (<nuke.nodes.Card>)
                The card whose plane we will create an axis on.
    
            offset : (float, float)
                Offset in (x, y) from center of card.
    
            parent_axis : (<nuke.nodes.Axis>)
                The axis that this axis should inherit transforms from.
    
            name : (str)
                What to name the resulting node.
    
            xform=True : (bool)
                If True, set the transform order.
    
        Returns:
            (<nuke.nodes.Axis>)
                An axis, attached to the parent_axis, that represents a point on
                the card plane as defined by the offset.
    
        Raises:
            N/A
    
        """
        axis = nuke.nodes.Axis()
        if xform:
            axis['xform_order'].setValue(1)
    
        card_width = float(card.width())
        card_height = float(card.height())
        card_aspect = card_height/card_width
        card_uniform_scale = card['uniform_scale'].value()
        card_scaling_x = card['scaling'].value(0)
        card_scaling_y = card['scaling'].value(1)
    
        axis['translate'].setValue(
            [
                offset[0] * card_uniform_scale * card_scaling_x,
                offset[1] * card_aspect * card_uniform_scale * card_scaling_y,
                0
            ]
        )
        axis.setInput(0, parent_axis)
        axis['name'].setValue(name)
    
        return axis
    
    # =============================================================================
    
    
    def _create_reconcile3D(axis, camera, background, name):
        """Creates a reconcile3D node attached to the axis
    
        Args:
            axis : (<nuke.nodes.Axis>)
                The axis node to create a 2d tracking point from.
    
            camera : (<nuke.nodes.Camera2>)
                The camera node to track through.
    
            background : (<nuke.node>)
                Any image node with a resolution.
    
            name : (str)
                What the name the resulting Reconcile3D node.
    
        Returns:
            (<nuke.nodes.Reconcile3D>)
                The incoming axis as a 2d track.
    
        Raises:
            N/A
    
        """
        track = nuke.nodes.Reconcile3D()
        track.setInput(2, axis)
        track.setInput(1, camera)
        track.setInput(0, background)
        track['name'].setValue(name)
    
        return track
    
    # =============================================================================
    # PUBLIC FUNCTIONS
    # =============================================================================
    
    
    def card_to_track(card, camera, background):
        """Takes the corners of a card and convert it to a variety of 2D outputs
    
        Args:
            card : (<nuke.nodes.Card2>)
                The card whose corners we wish to track.
    
            camera : (<nuke.nodes.Camera2>)
                The camera with the motion we want to track the card through.
    
            background : (<nuke.Node>)
                An image type background we can use to determine the format
                for the trackers.
    
        Returns:
            (<nuke.nodes.Tracker3>|<nuke.nodes.CornerPin2D>|<nuke.nodes.Roto>)
                The selected node types (or all) will be returned.
    
        Raises:
            N/A
    
        """
    
        # Open a panel to grab our required settings and return a dictionary.
        settings = _card_to_track_panel()
        if not settings:  # If panel canceled, we'll cancel.
            return
    
        # Turn our frame range into a nuke.FrameRange object we can iterate over.
        frange = nuke.FrameRange(settings['frange'])
    
        # Card values
        card_pos_x = card['xpos'].value()
        card_pos_y = card['ypos'].value()
        card_translate = card['translate'].value()
        card_rotate = card['rotate'].value()
        card_label = card['label'].value()
    
        # Create our Main Axis node
        main_axis = nuke.nodes.Axis()
        main_axis['xform_order'].setValue(3)
        main_axis['translate'].setValue(card_translate)
        main_axis['rotate'].setValue(card_rotate)
        main_axis['name'].setValue("MainAxis")
        main_axis['xpos'].setValue(card_pos_x)
        main_axis['ypos'].setValue(card_pos_y + 40)
    
        # Full card_to_track:
        if not settings['axis']:
    
            # Check if our card translates in space
            if card['translate'].isAnimated():
                main_axis['translate'].copyAnimations(
                    card['translate'].animations()
                )
    
            # Check if our card rotates in space
            if card['rotate'].isAnimated():
                main_axis['rotate'].copyAnimations(
                    card['rotate'].animations()
                )
    
            # TODO: What about animated scaling?
    
            # Create our axes at the corners of the card.
            upper_left = _create_axis(
                card, (-0.5, 0.5), main_axis, 'UpperLeft'
            )
            upper_right = _create_axis(
                card, (0.5, 0.5), main_axis, 'UpperRight'
            )
            lower_left = _create_axis(
                card, (-0.5, -0.5), main_axis, 'LowerLeft', False
            )
            lower_right = _create_axis(
                card, (0.5, -0.5), main_axis, 'LowerRight', False
            )
    
            axes = [upper_left, upper_right, lower_left, lower_right]
    
            # Position our axes nicely
            for i, axis in enumerate(axes):
                x = -100 if i % 2 else 100  # upper_left and lower_left
                y = -100 if i < 2 else 100  # upper_right and lower_right
                axis['xpos'].setValue(card_pos_x + x)
                axis['ypos'].setValue(card_pos_y + y)
    
            # Crate our reconcile3D nodes pointing to those axes
            upper_left_track = _create_reconcile3D(
                upper_left, camera, background, "UpperLeftTrack"
            )
            upper_right_track = _create_reconcile3D(
                upper_right, camera, background, "UpperRightTrack"
            )
            lower_left_track = _create_reconcile3D(
                lower_left, camera, background, "LowerLeftTrack"
            )
            lower_right_track = _create_reconcile3D(
                lower_right, camera, background, "LowerRightTrack"
            )
    
            tracks = [
                lower_left_track, lower_right_track,
                upper_right_track, upper_left_track,
            ]
    
            # Position our reconcile3D nodes
            for i, track in enumerate(tracks):
                x = -110 if i % 3 else 90  # lower_left and upper_left
                y = 160 if i < 2 else -40  # lower_left and lower_right
                track['xpos'].setValue(card_pos_x + x)
                track['ypos'].setValue(card_pos_y + y)
    
            # Evaluate our Reconciles for each frame
            for reconcile in tracks:
                nuke.execute(reconcile, settings['first'], settings['last'])
    
            if settings['output'] in ['All', 'Tracker']:
                tracker = reconcile_to_tracks(
                    inputs=tracks,
                    pos=(card_pos_x - 150, card_pos_y + 60),
                    label=card_label
                )
                if settings['output'] == 'Tracker':
                    # Cleanup our created nodes
                    for node in axes + tracks:
                        nuke.delete(node)
                    nuke.delete(main_axis)
                    return tracker
    
            # We always need a default corner_pin node for any of the remaining
            # export types.
            corner_pin = reconcile_to_corner(
                inputs=tracks,
                ref_frame=settings['ref_frame'],
                pos=(card_pos_x - 50, card_pos_y + 60),
                label=card_label
            )
    
            # Cleanup our created nodes, as we don't need them anymore.
            for node in axes + tracks:
                nuke.delete(node)
            nuke.delete(main_axis)
    
            if settings['output'] == 'CornerPin':
                return corner_pin
    
            corner_matrix = corner_pin_to_corner_matrix(
                corner_pin=corner_pin,
                frange=frange,
                pos=(card_pos_x + 50, card_pos_y + 60),
                label=card_label
            )
    
            if settings['output'] == "CornerPin(matrix)":
                # No longer need corner_pin
                nuke.delete(corner_pin)
                return corner_matrix
    
            roto = matrix_to_roto_matrix(
                matrix=corner_matrix,
                frange=frange,
                pos=(card_pos_x + 150, card_pos_y + 60),
                label=card_label
            )
    
            if settings['output'] == "Roto":
                # No longer need corner_pin
                nuke.delete(corner_pin)
                nuke.delete(corner_matrix)
                return roto
    
            # Only output left is 'All'
            return tracker, corner_pin, corner_matrix, roto
    
        # Here we'll only do translation
        else:
    
            main_track = _create_reconcile3D(main_axis, "MainTrack")
            nuke.execute(main_track, settings['first'], settings['last'])
    
            tracker = reconcile_to_tracks(
                inputs=[main_track],
                pos=(card_pos_x, card_pos_y + 60),
                label=card_label,
                translate_only=True
            )
    
            # cleanup
            nuke.delete(main_axis)
            nuke.delete(main_track)
    
            return tracker
    
    # =============================================================================
    
    
    def card_to_track_wrapper():
        """A wrapper for card_to_track that handles node selection
    
        Args:
            N/A
    
        Returns:
            None
    
        Raises:
            N/A
    
        """
        # Grab our selected nodes, there should only be three and we'll iterate
        # over them to determine which is which.
        nodes = nuke.selectedNodes()
    
        if len(nodes) != 3:
            nuke.message(
                "Please make sure you've selected a camera, an undisto and the "
                "card you wish to track"
            )
            return
    
        camera = None
        card = None
        background = None
    
        # Assign all of our required nodes to variables
        for node in nodes:
            if node.Class() == 'Camera2':
                camera = node
            elif node.Class() == 'Card2':
                card = node
            else:
                background = node
    
        # Check that we have a node at each variable
        if not camera or not card or not background:
            nuke.message(
                "No {camera}{cc}{card}{cb}{background} selected. Please select a "
                "camera, a background, and the card you wish to track.".format(
                    camera='camera' if not camera else '',
                    cc=', ' if not camera and not card else '',
                    card='card' if not card else '',
                    cb=', ' if (not camera or not card) and not background else '',
                    background='background' if not background else ''
                )
            )
            return
        else:
            card_to_track(card, camera, background)
    
    # =============================================================================
    
    
    def corner_pin_to_corner_matrix(corner_pin, frange, pos=None, label=None):
        """Transforms a CornerPin's to and from corners into a matrix
    
        Args:
            corner_pin : (<nuke.nodes.CornerPin2D>)
                The corner_pin node whose corners we want to create a
                transformation matrix from.
    
            frange : (<nuke.FrameRange>|[int])
                The frame range to grab the values from.
    
            pos=None : (int, int)
                An x, y position to place the node at.
    
            label=None : (str)
                What to label the created node.
    
        Returns:
            (<nuke.nodes.CornerPin2D>)
                A corner pin node with the to/from values not set, but the
                transformation matrix set.
    
        Raises:
            N/A
    
        """
        # Create our camera matrix
        to_matrix = nuke.math.Matrix4()
        from_matrix = nuke.math.Matrix4()
    
        corner_new = nuke.nodes.CornerPin2D()
        corner_new['transform_matrix'].setAnimated()
        if pos:
            corner_new['xpos'].setValue(pos[0])
            corner_new['ypos'].setValue(pos[1])
        corner_new['label'].setValue(
            "{label}Matrix".format(
                label=label if label else 'CornerPin'
            )
        )
    
        for frame in frange:
    
            # We'll grab all of our current frame's corners using
            # some list comprehensions.
            to_corners = [
                corner_pin[knob].valueAt(frame) for knob in [
                    'to1', 'to2', 'to3', 'to4'
                ]
            ]
            # This will return a list with 4 elements, but those
            # elements will be a tuple pair. We need to unpack the two
            # members of each tuple into a flat list.
            to_corners = [
                value for values in to_corners for value in values
            ]
    
            # Same as the above. We get a list with tuple elements, then
            # unpack it into a flat list.
            from_corners = [
                corner_pin[knob].valueAt(frame) for knob in [
                    'from1', 'from2', 'from3', 'from4'
                ]
            ]
            from_corners = [
                value for values in from_corners for value in values
            ]
    
            # Pass our flat lists into the matrix methods.
            to_matrix.mapUnitSquareToQuad(*to_corners)
            from_matrix.mapUnitSquareToQuad(*from_corners)
    
            corner_pin_matrix = to_matrix * from_matrix.inverse()
            corner_pin_matrix.transpose()
    
            for i in xrange(16):
                corner_new['transform_matrix'].setValueAt(
                    corner_pin_matrix[i],
                    frame,
                    i
                )
    
        return corner_new
    
    # =============================================================================
    
    
    def matrix_to_roto_matrix(matrix, frange, pos=None, label=None):
        """Copies a transform matrix from a node to a roto node with a matrix
    
        Args:
            matrix : (<nuke.Node>)
                Any node with the 'transform_matrix' knob.
    
            frange : (<nuke.FrameRange>|[int])
                The frame range to grab the values from.
    
            pos=None : (int, int)
                An x, y position to place the node at.
    
            label=None : (str)
                What to label the created node.
    
        Returns:
            (<nuke.nodes.Roto>)
                The resultant roto node with the transform matrix baked in.
    
        Raises:
            N/A
    
        """
        roto = nuke.nodes.Roto()
        if pos:
            roto['xpos'].setValue(pos[0])
            roto['ypos'].setValue(pos[1])
        if label:
            roto['label'].setValue(label)
    
        transform = roto['curves'].rootLayer.getTransform()
    
        for frame in frange:
    
            matrices = [
                matrix['transform_matrix'].getValueAt(
                    frame, i
                ) for i in xrange(16)
            ]
    
            for i, value in enumerate(matrices):
                matrix_curve = transform.getExtraMatrixAnimCurve(0, i)
                matrix_curve.addKey(frame, value)
    
        return roto
    
    # =============================================================================
    
    
    def reconcile_to_corner(inputs, ref_frame, pos=None, label=None):
        """Creates a CornerPin from 4 reconcile3D nodes
    
        Args:
            inputs : [<nuke.nodes.Reconcile3D>]
                A list of exactly 4 Reconcile3D nodes, corresponding to the
                desired corners of the corner pin.
    
                Order should be:
                Lower left, lower right, upper right, upper left
                (Counter clockwise starting from lower left)
    
            ref_frame : (int)
                Reference frame to key corner pin to.
    
            pos=None : (int, int)
                Position to place returned CornerPin
    
            label=None : (str)
                What to label the node (in addition to a read out of the
                ref_frame value).
    
        Returns:
            (<nuke.nodes.CornerPin2D>)
                CornerPin node with animated 'to' fields, and 'from' fields set
                to the ref_frame value.
    
        Raises:
            ValueError
                If given less than or more than 4 Reconcile3D nodes in inputs.
    
        """
    
        if len(inputs) != 4:
            raise ValueError(
                "create_tracks needs exactly 4 Reconcile3D nodes in the 'inputs' "
                "arg. Number of Reconcile3D nodes provided: "
                "{tracks_length}".format(
                    tracks_length=len(inputs)
                )
            )
    
        corner = nuke.nodes.CornerPin2D()
        if pos:
            corner['xpos'].setValue(pos[0])
            corner['ypos'].setValue(pos[1])
    
        corner["label"].setValue(
            "{label}ref frame: {ref_frame}".format(
                label=label + ' ' if label else '',
                ref_frame=ref_frame
            )
        )
    
        for i in xrange(4):
            to_knob = "to{0}".format(i + 1)
            from_knob = "from{0}".format(i + 1)
    
            corner[to_knob].copyAnimations(inputs[i]['output'].animations())
            corner[from_knob].setValue(inputs[i]['output'].getValueAt(ref_frame))
    
        return corner
    
    # =============================================================================
    
    
    def reconcile_to_tracks(inputs, pos=None, label=None, translate_only=False):
        """Creates a tracking node with track information from tracks
    
        Args:
            inputs : [<nuke.nodes.Reconcile3D>]
                A list of up to 4 Reconcile3D nodes to add trackers for.
    
            pos=None : (int, int)
                Position to place returned tracker.
    
            label=None : (str)
                What to label the node.
    
            translate_only=False (bool)
                If True, each tracker will be set only affect translation, not
                rotation or sale.
    
        Returns:
            (<nuke.nodes.Tracker3>)
                Tracker node with the input Reconcile3D tracks being the trackers.
    
        Raises:
            ValueError
                If tracks has more than 4 members.
    
        """
        if len(inputs) > 4:
            raise ValueError(
                "reconcile_to_tracks takes at most 4 Reconcile3D nodes in the "
                "'inputs' arg. Number of Reconcile3D nodes provided: "
                "{tracks_length}".format(
                    tracks_length=len(inputs)
                )
            )
    
        tracker = nuke.nodes.Tracker3()
        if pos:
            tracker['xpos'].setValue(pos[0])
            tracker['ypos'].setValue(pos[1])
        if label:
            tracker['label'].setValue(label)
    
        for i in xrange(len(inputs)):
            enable_knob = 'enable{0}'.format(i + 1)
            track_knob = 'track{0}'.format(i + 1)
            use_knob = 'use_for{0}'.format(i + 1)
    
            tracker[enable_knob].setValue(1)
            tracker[track_knob].copyAnimations(inputs[i]['output'].animations())
            if not translate_only:
                tracker[use_knob].setValue(7)
    
        return tracker
    
    card_to_track_wrapper()
main()