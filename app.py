import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from start import StartUI

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.v = {'useSubDir': True, 'dir': '', 'images': []}
        self.exts = ['png', 'jpg', 'jpeg']
        self.initUI()

    def initUI(self):
        self.setWindowTitle('image-classifier')
        self.setCentralWidget(StartUI(self))
        self.resize(640, 360)
        self.center()
        self.show()

    def center(self):
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def state(self, key, state):
        self.v[key] = state == Qt.Checked;


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
