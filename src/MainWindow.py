# -*- coding: utf-8 -*-
from src.Ui.Ui_MainWindow import Ui_MainWindow
from src.NGA_Spider import *
from src.CheckDialog import *
from PyQt5.QtWidgets import *
import json
from bs4 import BeautifulSoup
import re


class MainWindow(QMainWindow):
    guns = dict()
    name2guns = dict()
    tid = 17315247
    pages = 1
    schedule = "1"
    truelove_info = dict()
    vote = dict()
    truelove_vote = dict()

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
        self.tid = int(self.ui.tidLineEdit.text())
        self.pages = int(self.ui.pagesLineEdit.text())
        self.schedule = self.ui.scheduleLineEdit.text()
        self.make_name2guns()
        self.truelove_info.clear()
        for p in range(1, self.pages + 1):
            self.process_page("https://bbs.nga.cn/read.php?tid=%d&page=%d" % (self.tid, p))

    # 处理一页的信息
    def process_page(self, url):
        html_str = down_web(url)
        if html_str is None:
            return
        soup = BeautifulSoup(html_str, 'lxml')
        tables = soup.find_all('table')
        for table in tables:
            cls = table.get('class')
            if cls[0] == 'forumbox':
                tds = table.find_all('td')
                script = tds[1].find('script')
                if script:
                    self.process_main_floor(script)
                else:
                    self.process_comment(tds)

    # 处理主楼的投票数据
    def process_main_floor(self, script):
        t = script.split(',', 2)
        t = t[2].split('\'')
        data = t[1].split('~')
        id_list = dict()
        for i in range(0, len(data), 2):
            if data[i].isnumeric():
                # 登记数字编号与文本的对应
                id_list[data[i]] = data[i + 1]
            elif data[i].find('max_select') >= 0:
                # 跳过max_select语句
                i += 2
            else:
                # 处理投票数量
                vote = data[i + 1].split(',')[0]
                self.vote[self.name2guns[id_list[data[i][1:]]]] = int(vote)

    # 处理回复的真爱数据
    def process_comment(self, tds):
        found = set()
        truelove = ''
        spans = tds[1].find_all('span')
        if len(spans) < 2:
            return
        sp = spans[1].span
        if sp:
            cmt = sp.get_text()
            pattern = re.compile(r'uid=([\d]+)')
            uid = pattern.findall(tds[0].find('span').find('a').get('href'))[0]
            for name in self.name2guns:
                if str.find(cmt, name) >= 0:
                    found.add(self.name2guns[name])
                    truelove = self.name2guns[name]
            if len(found) != 1:
                # 弹窗选择
                truelove = CheckDialog.pop(self, cmt)
            if (uid in self.truelove_info) and (self.truelove_info[uid] != truelove):
                # 清空该uid所有的信息，并且空串以后也一直会进入该分支
                self.truelove_info = ''
                truelove = ''
            if truelove in self.name2guns:
                self.truelove_vote[truelove] += 1

    def load_setting(self):
        filename, _ = QFileDialog.getOpenFileName(self, filter="JSON(*.json)")
        with open(filename, 'r', encoding='gbk') as fin:
            settings = json.load(fin, encoding='gbk')
            self.ui.tidLineEdit.setText(settings['tid'])
            self.ui.pagesLineEdit.setText(settings['pages'])
            self.ui.scheduleLineEdit.setText(settings['schedule'])
            self.ui.trueloveLineEdit.setText(settings['truelove'])
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
            'tid': self.ui.tidLineEdit.text(),
            'pages': self.ui.pagesLineEdit.text(),
            'schedule': self.ui.scheduleLineEdit.text(),
            'guns': self.guns,
            'truelove': self.ui.trueloveLineEdit.text()
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

    # 制作昵称到枪的反向对应
    def make_name2guns(self):
        self.name2guns.clear()
        self.vote.clear()
        self.truelove_vote.clear()
        for gun in self.guns:
            for name in self.guns[gun]:
                self.name2guns[name] = gun
            self.vote[gun] = 0
            self.truelove_vote[gun] = 0
