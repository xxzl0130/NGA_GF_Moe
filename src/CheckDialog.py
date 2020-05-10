from src.Ui.Ui_CheckDialog import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class CheckDialog(QDialog):
    def __init__(self, parent=None):
        super(CheckDialog, self).__init__(parent)
        self.ui = Ui_CheckDialog()
        self.ui.setupUi(self)
        self.ui.confirmPushButton.clicked.connect(self.accept)

    @staticmethod
    def pop(parent, cmt):
        dialog = CheckDialog(parent)
        dialog.ui.cmtTextEdit.setPlainText(cmt)
        dialog.exec()
        return dialog.ui.voteLineEdit.text()
