# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CheckDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CheckDialog(object):
    def setupUi(self, CheckDialog):
        CheckDialog.setObjectName("CheckDialog")
        CheckDialog.resize(400, 340)
        self.verticalLayout = QtWidgets.QVBoxLayout(CheckDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CheckDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.cmtTextEdit = QtWidgets.QPlainTextEdit(CheckDialog)
        self.cmtTextEdit.setReadOnly(True)
        self.cmtTextEdit.setObjectName("cmtTextEdit")
        self.verticalLayout.addWidget(self.cmtTextEdit)
        self.label_2 = QtWidgets.QLabel(CheckDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.voteLineEdit = QtWidgets.QLineEdit(CheckDialog)
        self.voteLineEdit.setObjectName("voteLineEdit")
        self.verticalLayout.addWidget(self.voteLineEdit)
        self.label_3 = QtWidgets.QLabel(CheckDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.nameLineEdit = QtWidgets.QLineEdit(CheckDialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.verticalLayout.addWidget(self.nameLineEdit)
        self.confirmPushButton = QtWidgets.QPushButton(CheckDialog)
        self.confirmPushButton.setObjectName("confirmPushButton")
        self.verticalLayout.addWidget(self.confirmPushButton)

        self.retranslateUi(CheckDialog)
        QtCore.QMetaObject.connectSlotsByName(CheckDialog)

    def retranslateUi(self, CheckDialog):
        _translate = QtCore.QCoreApplication.translate
        CheckDialog.setWindowTitle(_translate("CheckDialog", "人工复核"))
        self.label.setText(_translate("CheckDialog", "原始评论："))
        self.label_2.setText(_translate("CheckDialog", "投票对象，留空则无:"))
        self.label_3.setText(_translate("CheckDialog", "文中昵称，用于补充列表，可不填:"))
        self.confirmPushButton.setText(_translate("CheckDialog", "确定"))
