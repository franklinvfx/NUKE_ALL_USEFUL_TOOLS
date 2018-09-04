#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Next bokeh
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('bokeh_choice').setValue (+1 +(i.knob('bokeh_choice').value()))