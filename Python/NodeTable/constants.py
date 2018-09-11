"""Define all constant variables here, to avoid magic numbers."""

# pylint: disable=import-error
import nuke

PACKAGE_NICE_NAME = 'Node Spreadsheet'

FILTER_DELIMITER = ','

# Knob classes that can't be edited directly
READ_ONLY_KNOBS = [nuke.Transform2d_Knob]

# Colors
# knob is animated
KNOB_ANIMATED_COLOR = (0.312839, 0.430188, 0.544651)
# knob has key at current frame
KNOB_HAS_KEY_AT_COLOR = (0.165186, 0.385106, 0.723738)

# Mix background color with node color by this amount
# if cell has no knob:
CELL_MIX_NODE_COLOR_AMOUNT_NO_KNOB = .08
# if cell has knob:
CELL_MIX_NODE_COLOR_AMOUNT_HAS_KNOB = 0.3

# Editors:
# Cell size:
EDITOR_CELL_WIDTH = 80
EDITOR_CELL_HEIGHT = 28

# editor precision
EDITOR_DECIMALS = 8

# Ask for user confirmation before loading more than this many nodes.
NUM_NODES_WARN_BEFORE_LOAD = 50

# Shading mode follows preferences when not in non-commercial mode.
# Skip checking the preferences node since that counts towards the
# 10 nodes limit in non-commercial edition.
SHADE_DAG_NODES_NON_COMMERCIAL = True
