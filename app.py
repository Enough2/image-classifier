import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from start import StartUI
from classify import ClassifyUI

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.v = {'useSubDir': True, 'dir': '', 'images': []}
        self.exts = ['png', 'jpg', 'jpeg']
        self.toolBar = None
        self.progressBar = None
        self.thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('image-classifier')
        self.changeScene(StartUI)
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

    def changeScene(self, scene):
        if self.toolBar:
            self.removeToolBar(self.toolBar)
        self.statusBar().clearMessage()
        self.statusBar().removeWidget(self.progressBar)
        self.setCentralWidget(scene(self))

    def selectDir(self):
        dir = QFileDialog.getExistingDirectory(self, '분류할 이미지 폴더 선택하기')
        if dir:
            self.v['dir'] = dir
            if self.thread:
                self.thread.stop()
            self.changeScene(ClassifyUI)



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
