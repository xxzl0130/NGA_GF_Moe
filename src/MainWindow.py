# -*- coding: utf-8 -*-
from src.Ui.Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json


class MainWindow(QMainWindow):
    guns = dict()

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect()

    def connect(self):
        self.ui.startPushButton.clicked.connect(self.start)
        self.ui.loadSettingPushButton.clicked.connect(self.load_setting)
        self.ui.saveSettingPushButton.clicked.connect(self.save_setting)
        self.ui.addGunPushButton.clicked.connect(self.add_gun)
        self.ui.delGunPushButton.clicked.connect(self.del_gun)
        self.ui.addNamePushButton.clicked.connect(self.add_name)
        self.ui.delNamePushButton.clicked.connect(self.del_name)
        self.ui.gunListWidget.currentTextChanged.connect(self.select_gun)

    def start(self):
        # TODO
        return

    def load_setting(self):
        filename, _ = QFileDialog.getOpenFileName(self, filter="JSON(*.json)")
        with open(filename, 'r', encoding='gbk') as fin:
            settings = json.load(fin, encoding='gbk')
            self.ui.fidLineEdit.setText(settings['fid'])
            self.ui.pagesLineEdit.setText(settings['pages'])
            self.ui.scheduleLineEdit.setText(settings['schedule'])
            guns = settings["guns"]
            for gun in guns:
                self.ui.gunLineEdit.setText(gun)
                self.add_gun()
                self.del_name()
                names = guns[gun]
                for name in names:
                    self.ui.nameLineEdit.setText(name)
                    self.add_name()

    def save_setting(self):
        settings = {
            'fid': self.ui.fidLineEdit.text(),
            'pages': self.ui.pagesLineEdit.text(),
            'schedule': self.ui.scheduleLineEdit.text(),
            'guns': self.guns
        }
        data = json.dumps(settings, ensure_ascii=False)
        filename, _ = QFileDialog.getSaveFileName(self, filter="JSON(*.json)")
        with open(filename, 'w', encoding='gbk') as fout:
            fout.write(data)
            fout.close()

    def add_gun(self):
        gun = self.ui.gunLineEdit.text()
        if gun not in self.guns:
            self.guns[gun] = []
            self.ui.gunListWidget.addItem(gun)
            self.ui.gunListWidget.setCurrentRow(len(self.guns) - 1)
            self.ui.gunLineEdit.clear()
            self.ui.nameLineEdit.setText(gun)
            self.add_name()

    def del_gun(self):
        gun = self.ui.gunListWidget.currentItem().text()
        self.guns.pop(gun)
        self.ui.gunListWidget.takeItem(self.ui.gunListWidget.currentRow())

    def add_name(self):
        if self.ui.gunListWidget.currentRow() < 0:
            return
        gun = self.ui.gunListWidget.currentItem().text()
        name = self.ui.nameLineEdit.text()
        self.guns[gun].append(name)
        self.ui.nameListWidget.addItem(name)
        self.ui.nameLineEdit.clear()
        self.ui.nameListWidget.setCurrentRow(len(self.guns[gun]) - 1)

    def del_name(self):
        gun = self.ui.gunListWidget.currentItem().text()
        del self.guns[gun][self.ui.nameListWidget.currentRow()]
        self.ui.nameListWidget.takeItem(self.ui.nameListWidget.currentRow())

    def select_gun(self, gun):
        if gun not in self.guns:
            return
        names = self.guns[gun]
        self.ui.nameListWidget.clear()
        self.ui.nameListWidget.addItems(names)

