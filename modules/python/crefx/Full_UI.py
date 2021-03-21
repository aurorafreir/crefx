from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
import os

from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

### UI to-do
# todo add image to UI using pyside qImage

### CODE to-do
# todo set up code for arms
# todo set up code for spine
# todo set up code for leg
# todo set up code for tail
# todo set up code for hand
# todo set up code for


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class BlockBuilder(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(BlockBuilder, self).__init__()
        self.create_widget()
        #self.create_connections()

    def create_widget(self):
        self.setWindowFlags(QtCore.Qt.Tool)

        self.setParent(maya_main_window())
        self.setWindowFlags(QtCore.Qt.Window)

        # Set the object name
        self.setObjectName('CreateFullUI_UniqueId')
        self.setWindowTitle('Create Block')
        self.setGeometry(100, 100, 500, 250)
        self.setMinimumSize(200, 200)

        #pixmap = QtGui.QPixmap('/home/aurorafreir/Pictures/2020-08-29_16-05.png')
        #self.label = QtWidgets.QLabel()
        #self.label.setPixmap(pixmap)
        #self.label.show()

        #pixmap = QtGui.QPixmap('/data/Top_UI.jpeg')
        UIImagePath = os.path.abspath(os.path.join(__file__, '..', '..', 'data/Top_UI.jpg'))
        self.UIImage = QtWidgets.QLabel()
        self.UIImage.setPixmap(UIImagePath)
        self.UIImage.setGeometry(0, 0, 400, 60)
        self.UIImage.setParent(self)

        # button to call the buildBlock function
        self.button = QtWidgets.QPushButton(self, text="Build")
        self.button.setGeometry(50, 200, 150, 30)



# Call the UI to start

if cmds.window("CreateBlockUI_UniqueIdWorkspaceControl", exists=True):
    cmds.deleteUI("CreateBlockUI_UniqueIdWorkspaceControl")

ui = BlockBuilder()
ui.show()

#print __file__