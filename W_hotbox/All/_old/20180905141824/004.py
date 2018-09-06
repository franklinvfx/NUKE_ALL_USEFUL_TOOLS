#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Select Dependencies
#
#----------------------------------------------------------------------------------------------------------

from cgev.nuke.tools.nodes import operations

for node in nuke.selectedNodes():
    operations.selectDependencies(node)