"""A Table to display and edit nukes Nodes."""

import logging

# python 3 compatibility
# @TODO: find a better way
try:
    basestring
except NameError:
    #pylint: disable=redefined-builtin, invalid-name
    basestring = str

logging.getLogger(__name__).addHandler(logging.NullHandler())
