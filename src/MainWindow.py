# -*- coding: utf-8 -*-
from src.Ui.Ui_MainWindow import Ui_MainWindow
from src.NGA_Spider import *
from src.CheckDialog import *
from PyQt5.QtWidgets import *
import json
from bs4 import BeautifulSoup
import re
import os
import time

data_dir = './data'
duplicate_str = '!@#err!duplicate!err!!@#'  # 标记重复投票的字符串


class MainWindow(QMainWindow):
    # 名字到昵称的对应
    guns = dict()
    # 昵称到名字的对应
    name2guns = dict()
    tid = 17315247
    pages = 1
    schedule = "1"
    # 记录uid选择的真爱票，需要读完所有回复之后再记录
    truelove_info = dict()
    # 普通投票数量
    vote = dict()
    # 真爱票数量
    truelove_vote = dict()
    # 记录uid，回复，对应的角色
    comment_log = []
    # 记录最大楼层号
    max_floor = 0
    # 记录楼层序号
    floors = []

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect()
        self.init_table()
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

    def connect(self):
        self.ui.startPushButton.clicked.connect(self.start)
        self.ui.loadSettingPushButton.clicked.connect(self.load_setting)
        self.ui.saveSettingPushButton.clicked.connect(self.save_setting)
        self.ui.addGunPushButton.clicked.connect(self.add_gun)
        self.ui.delGunPushButton.clicked.connect(self.del_gun)
        self.ui.addNamePushButton.clicked.connect(self.add_name)
        self.ui.delNamePushButton.clicked.connect(self.del_name)
        self.ui.gunListWidget.currentTextChanged.connect(self.select_gun)

    def init_table(self):
        self.ui.voteTableWidget.clear()
        self.ui.voteTableWidget.setColumnCount(4)
        self.ui.voteTableWidget.setHorizontalHeaderLabels(['角色', '普通票', '真爱票', '总票数'])
        self.ui.voteTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.voteTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.voteTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.voteTableWidget.setSortingEnabled(True)

    def start(self):
        self.tid = int(self.ui.tidLineEdit.text())
        self.pages = int(self.ui.pagesLineEdit.text())
        self.schedule = self.ui.scheduleLineEdit.text()
        self.init()
        for p in range(1, self.pages + 1):
            self.process_page("https://bbs.nga.cn/read.php?tid=%d&page=%d" % (self.tid, p))
        for uid in self.truelove_info:
            gun = self.truelove_info[uid]
            if gun in self.guns:
                self.truelove_vote[gun] += 1
        # 更新统计表
        self.update_table()
        self.export_cmt_log()
        self.export_floor_info()

    def update_table(self):
        truelove_rate = int(self.ui.trueloveLineEdit.text())
        self.init_table()
        row = 0
        self.ui.voteTableWidget.setRowCount(len(self.guns))
        fout = open(data_dir + '/' + self.ui.scheduleLineEdit.text() + '-' + self.get_time() + '-统计' + '.csv', 'w',
                    encoding='gbk')
        fout.write('角色,普通票,真爱票,总票数\n')
        for gun in self.guns:
            self.ui.voteTableWidget.setItem(row, 0, QTableWidgetItem(gun))
            vote = self.vote[gun]
            self.ui.voteTableWidget.setItem(row, 1, QTableWidgetItem("%d" % vote))
            truelove = self.truelove_vote[gun]
            self.ui.voteTableWidget.setItem(row, 2, QTableWidgetItem("%d" % truelove))
            sum = vote + truelove * truelove_rate
            self.ui.voteTableWidget.setItem(row, 3, QTableWidgetItem("%d" % sum))
            fout.write("%s,%d,%d,%d\n" % (gun, vote, truelove, sum))
            row += 1
        fout.close()

    def export_cmt_log(self):
        fout = open(data_dir + '/' + self.ui.scheduleLineEdit.text() + '-' + self.get_time() + '-明细' + '.csv', 'w',
                    encoding='gbk')
        fout.write('楼层,UID,原始评论,真爱票\n')
        for it in self.comment_log:
            fout.write('%s,%s,%s,%s\n' % (it[0], it[1], str.replace(it[2], '\n', ''), it[3]))
        fout.close()
        fout = open(data_dir + '/' + self.ui.scheduleLineEdit.text() + '-' + self.get_time() + '-重复' + '.txt', 'w',
                    encoding='gbk')
        for uid in self.truelove_info:
            if self.truelove_info[uid] == duplicate_str:
                fout.write(uid + '\n')
        fout.close()

    # 输出缺少的楼层
    def export_floor_info(self):
        fout = open(data_dir + '/' + self.ui.scheduleLineEdit.text() + '-' + self.get_time() + '-缺楼' + '.txt', 'w',
                    encoding='gbk')
        for i in range(1, self.max_floor):
            if i not in self.floors:
                fout.write("%d\n" % i)
        fout.close()

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
                if len(tds) < 2:
                    return
                script = tds[1].find('script')
                if script:
                    self.process_main_floor(script)
                else:
                    self.process_comment(tds)

    # 处理主楼的投票数据
    def process_main_floor(self, script):
        t = str.split(script.string, ',', 2)
        if len(t) < 2:
            return
        t = str.split(t[2], '\'')
        if len(t) <= 2:
            return
        data = str.split(t[1], '~')
        if len(data) <= 2:
            return
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
                name = id_list[data[i][1:]]
                if name not in self.name2guns:
                    continue
                self.vote[self.name2guns[name]] = int(vote)

    # 处理回复的真爱数据
    def process_comment(self, tds):
        found = set()
        truelove = ''
        spans = tds[1].find_all('span')
        if len(spans) < 2:
            return
        sp = spans[1].span
        if sp:
            cmt = self.trim_symbols(sp.get_text().lower())  # 全部转小写处理
            pattern = re.compile(r'uid=([\d]+)')
            uid = pattern.findall(tds[0].find('span').find('a').get('href'))[0]
            floor = int(tds[1].find_all('a')[1].get('name').replace('l', ''))
            self.floors.append(floor)
            if floor > self.max_floor:
                self.max_floor = floor
            for name in self.name2guns:
                if str.find(cmt, name) >= 0:
                    found.add(self.name2guns[name])
                    truelove = self.name2guns[name]
            if len(found) != 1:
                # 弹窗选择
                truelove, name = CheckDialog.pop(self, cmt)
                if truelove in self.name2guns:
                    truelove = self.name2guns[truelove]
                    name = name.strip()
                    if len(name) > 1:
                        # 把名字加到列表
                        self.ui.gunLineEdit.setText(truelove)
                        self.add_gun()
                        self.ui.nameLineEdit.setText(name)
                        self.add_name()

            if (uid in self.truelove_info) and (self.truelove_info[uid] != truelove):
                # 清空该uid所有的信息并记为重复，并且该串会使其以后也一直会进入该分支
                self.truelove_info[uid] = duplicate_str
            else:
                # 记录uid选择的真爱票
                self.truelove_info[uid] = truelove
            # 记录log
            self.comment_log.append([floor, uid, cmt, truelove])

    def load_setting(self):
        filename, _ = QFileDialog.getOpenFileName(self, filter="JSON(*.json)")
        if len(filename) < 1:
            return
        with open(filename, 'r', encoding='gbk') as fin:
            self.clear()
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
        gun = self.ui.gunLineEdit.text().strip()  # strip去除空格
        if gun not in self.guns:
            self.guns[gun] = []
            self.ui.gunListWidget.addItem(gun)
            self.ui.gunListWidget.setCurrentRow(len(self.guns) - 1)
            self.ui.gunLineEdit.clear()
            self.ui.nameLineEdit.setText(gun.lower())  # 昵称统一转小写
            self.add_name()
        else:
            for i in range(len(self.guns)):
                if self.ui.gunListWidget.item(i).text() == gun:
                    self.ui.gunListWidget.setCurrentRow(i)
                    self.ui.gunLineEdit.clear()
                    break

    def del_gun(self):
        gun = self.ui.gunListWidget.currentItem().text()
        self.guns.pop(gun)
        self.ui.gunListWidget.takeItem(self.ui.gunListWidget.currentRow())

    def add_name(self):
        if self.ui.gunListWidget.currentRow() < 0:
            return
        gun = self.ui.gunListWidget.currentItem().text()
        name = self.ui.nameLineEdit.text().lower()
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
        for gun in self.guns:
            for name in self.guns[gun]:
                self.name2guns[name] = gun
            self.vote[gun] = 0
            self.truelove_vote[gun] = 0

    # 清除所有信息
    def clear(self):
        self.floors.clear()
        self.max_floor = 0
        self.truelove_info.clear()
        self.comment_log.clear()
        self.name2guns.clear()
        self.guns.clear()
        self.vote.clear()
        self.truelove_vote.clear()
        self.pages = 0
        self.schedule = ''
        self.tid = 0
        self.init_table()
        self.ui.gunListWidget.clear()
        self.ui.nameListWidget.clear()
        self.ui.gunLineEdit.clear()
        self.ui.nameLineEdit.clear()

    # 统计前的初始化
    def init(self):
        self.floors.clear()
        self.max_floor = 0
        self.truelove_info.clear()
        self.comment_log.clear()
        self.vote.clear()
        self.truelove_vote.clear()
        self.make_name2guns()

    # 去除奇奇怪怪的符号
    @staticmethod
    def trim_symbols(text):
        symbols = [',', '!', '！', '？', '?', '~', '～', '+', '_', '—']
        for s in symbols:
            str.replace(text, s, '')
        return text

    @staticmethod
    def get_time():
        return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
