import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from start import StartUI
from classify import ClassifyUI

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.useSubDir = True
        self.dir = ""
        self.save = ""
        self.exts = ['png', 'jpg', 'jpeg']
        self.toolBar = None
        self.progressBar = None
        self.thread = None

        self.images = []
        self.labels = []
        self.classButtons = []
        self.tabs = []
        self.data = [[] for _ in range(15)]
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('image-classifier')
        self.changeScene(StartUI)
        self.setFixedSize(1280, 720)
        self.statusBar().setSizeGripEnabled(False)
        self.center()
        self.show()

    def center(self):
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def changeScene(self, scene):
        if self.toolBar:
            self.removeToolBar(self.toolBar)
        self.statusBar().clearMessage()
        self.statusBar().removeWidget(self.progressBar)
        self.setCentralWidget(scene(self))

    def selectDir(self):
        dir = QFileDialog.getExistingDirectory(self, '분류할 이미지 폴더 선택하기')
        if dir:
            self.dir = dir
            if self.thread:
                self.thread.stop()
            self.changeScene(ClassifyUI)



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
