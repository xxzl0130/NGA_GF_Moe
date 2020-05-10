from src.MainWindow import MainWindow
from PyQt5 import QtWidgets
import sys
from src.CheckDialog import *

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)