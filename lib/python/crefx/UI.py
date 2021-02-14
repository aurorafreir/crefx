from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore

from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class BlockBuilder(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(BlockBuilder, self).__init__()

        self.setParent(maya_main_window())
        self.setWindowFlags(QtCore.Qt.Window)

        # Set the object name
        self.setObjectName('CreateBlockUI_UniqueId')
        self.setWindowTitle('Create Block')
        self.setGeometry(50, 50, 250, 150)

        self.textField = QtWidgets.QLineEdit(self, text="L")
        self.textField.setGeometry(10, 10, 150, 30)
        self.textField = QtWidgets.QLineEdit(self, text="Shoulder")
        self.textField.setGeometry(10, 40, 150, 30)
        self.textField = QtWidgets.QLineEdit(self, text="Elbow")
        self.textField.setGeometry(10, 70, 150, 30)
        self.textField = QtWidgets.QLineEdit(self, text="Wrist")
        self.textField.setGeometry(10, 100, 150, 30)

        self.button = QtWidgets.QPushButton(self, text="Build")
        self.button.setGeometry(10, 130, 150, 30)

        self.button.clicked.connect(self.buildBlock)

    def buildBlock(self):
        prefix = self.textField().text()

        import crefx.blockBuilder as bb
        reload(bb)

        block = bb.ThreeJointIK(prefix=prefix)
        block.build()

        print "build block", name

try:
    ui.deleteLater()
except NameError as e:
    pass

ui = BlockBuilder()
ui.show()
