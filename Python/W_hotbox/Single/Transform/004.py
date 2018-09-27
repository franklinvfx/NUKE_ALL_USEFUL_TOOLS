#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Add ref frame
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    if node.knob('translate').hasExpression():
        origExpression = node.knob('translate').animation(0).expression()
        if '-' in origExpression:
            origExpression = origExpression.split('-')
            origExpression = origExpression[0]

        newExpression = "{exp}-({exp}({frame}))".format(exp=origExpression, frame=nuke.frame())
        node.knob('translate').animation(0).setExpression(newExpression)
    else:
        saveY = node.knob('translate').value(0)
        for key in node.knob('translate').animation(0).keys():
            node.knob('translate').setValueAt(key.y-saveY, key.x, 0)