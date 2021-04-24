from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
import os

from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

### UI to-do
# done add image to UI using pyside qImage

### CODE to-do
# todo set up code for interactive positions
# in progress todo set up code for spine
# todo set up code for arms
# todo set up code for leg
# todo set up code for tail
# todo set up code for hand


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class block_builder(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(block_builder, self).__init__()
        self.create_widget()
        #self.create_connections()

    def create_widget(self):
        self.setWindowFlags(QtCore.Qt.Tool)

        self.setParent(maya_main_window())
        self.setWindowFlags(QtCore.Qt.Window)

        # Set the object name
        self.setObjectName('CreateFullUI_UniqueId')
        self.setWindowTitle('Create Block')
        self.setGeometry(100, 100, 400, 600)
        self.setMinimumSize(400, 600)

        # Image at top of the UI
        ui_image_path = os.path.abspath(os.path.join(__file__, '..', '..', 'data/Top_UI.jpg'))
        self.ui_image = QtWidgets.QLabel()
        self.ui_image.setPixmap(ui_image_path)
        self.ui_image.setGeometry(0, 0, 400, 60)
        self.ui_image.setParent(self)


        ### Spine UI
        # text and textbox for spine start position
        self.spine_start_pos = QtWidgets.QLineEdit(self, text="0,0,0")
        self.spine_start_pos.setGeometry(80, 200, 60, 30)
        self.textPrefix = QtWidgets.QLabel(self, text="Start Position")
        self.textPrefix.setGeometry(10,200,70,30)

        # text and textbox for spine end position
        self.spine_end_pos = QtWidgets.QLineEdit(self, text="1,0,0")
        self.spine_end_pos.setGeometry(240, 200, 60, 30)
        self.textPrefix = QtWidgets.QLabel(self, text="End Position")
        self.textPrefix.setGeometry(170,200,70,30)

        # button to call the buildBlock function
        self.spineBuildButton = QtWidgets.QPushButton(self, text="Build Spine")
        self.spineBuildButton.setGeometry(300, 200, 100, 30)

        self.spineBuildButton.clicked.connect(self.build_spine_block)


        ### Arm UI
        # text and textbox for spine start position
        self.arm_start_pos = QtWidgets.QLineEdit(self, text="0,0,0")
        self.arm_start_pos.setGeometry(80, 240, 60, 30)
        self.textPrefix = QtWidgets.QLabel(self, text="Start Position")
        self.textPrefix.setGeometry(10,240,70,30)

        # text and textbox for spine end position
        self.spine_start_pos = QtWidgets.QLineEdit(self, text="1,0,0")
        self.spine_start_pos.setGeometry(240, 240, 60, 30)
        self.textPrefix = QtWidgets.QLabel(self, text="End Position")
        self.textPrefix.setGeometry(170,240,70,30)

        # button to call the buildBlock function
        self.armBuildButton = QtWidgets.QPushButton(self, text="Build Arm")
        self.armBuildButton.setGeometry(300, 240, 100, 30)

        self.armBuildButton.clicked.connect(self.build_arm_block)


    def build_spine_block(self):
        import crefx.buildSpine as cfxbs
        reload(cfxbs)

        block = cfxbs.build_spine()
        block.build_spine_block()

    def build_arm_block(self):
        pass
        import crefx.buildArm as cfxba
        reload(cfxba)

        block = cfxba.build_arm()
        block.build_arm_block()


# Call the UI to start

if cmds.window("CreateBlockUI_UniqueIdWorkspaceControl", exists=True):
    cmds.deleteUI("CreateBlockUI_UniqueIdWorkspaceControl")

ui = block_builder()
ui.show()
