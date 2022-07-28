import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class ClassifyUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.groups = {}
        self.initUI()

    def initUI(self):
        selectDir = QAction(QIcon('icons/folders.png'), '분류할 이미지 폴더 선택하기', self)
        selectDir.triggered.connect(self.p.selectDir)
        undoAction = QAction(QIcon('icons/arrow-back-up.png'), '취소', self)
        redoAction = QAction(QIcon('icons/arrow-forward-up.png'), '다시 실행', self)
        exitAction = QAction(QIcon('icons/logout.png'), '종료', self)
        exitAction.triggered.connect(self.p.close)

        self.p.toolBar = self.p.addToolBar('툴바')
        self.p.toolBar.addAction(selectDir)
        self.p.toolBar.addAction(undoAction)
        self.p.toolBar.addAction(redoAction)
        self.p.toolBar.addAction(exitAction)

        self.p.progressBar = QProgressBar()
        self.p.statusBar().addPermanentWidget(self.p.progressBar)

        self.createLayout()

        self.p.thread = ImportThread(self.p)
        self.p.thread.update.connect(lambda x: self.p.statusBar().showMessage(f"파일 불러오는 중... ({x:,}개)"))
        self.p.thread.finished.connect(lambda x: self.loadImages() if x else None)
        self.p.thread.start()

    def createLayout(self):
        grid = QGridLayout()

        self.groups['preview'] = QGroupBox('미리보기')
        self.groups['preview'].setFixedSize(self.groups['preview'].height(), self.groups['preview'].height())
        label = QLabel()
        label.setPixmap(QPixmap(""))
        label.setAlignment(Qt.AlignCenter)
        vBox = QVBoxLayout()
        vBox.addWidget(label)
        self.groups['preview'].setLayout(vBox)
        grid.addWidget(self.groups['preview'], 0, 0)

        self.groups['classify'] = QGroupBox('분류')
        vBox = QVBoxLayout()
        for i in range(10):
            vBox.addWidget(QPushButton(str(i)))
        self.groups['classify'].setLayout(vBox)
        grid.addWidget(self.groups['classify'], 0, 1)

        self.groups['file'] = QGroupBox('파일')
        vBox = QVBoxLayout()
        vBox.addWidget(QListWidget(self.groups['file']))
        self.groups['file'].setLayout(vBox)
        grid.addWidget(self.groups['file'], 0, 2)

        self.setLayout(grid)

    def loadImages(self):
        self.p.thread.stop()
        self.p.statusBar().showMessage(f"파일 불러오기 완료 ({len(self.p.v['images']):,}개)")

class ImportThread(QThread):
    update = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent

    def run(self):
        images = []

        self.p.progressBar.setRange(0, 0)
        self.p.progressBar.setValue(0)
        self.update.emit(0)

        if self.p.v['useSubDir']:
            for root, dirs, files in os.walk(self.p.v['dir']):
                for file in files:
                    if file.split('.')[-1] in self.p.exts:
                        images.append(os.path.join(root, file))
                        self.update.emit(len(images))
        else:
            for file in os.listdir(self.p.v['dir']):
                if file.split('.')[-1] in self.p.exts:
                    images.append(os.path.join(self.p.v['dir'], file))
                    self.update.emit(len(images))

        self.p.v['images'] = images
        self.finished.emit(True)
        self.p.progressBar.hide()

    def stop(self):
        self.terminate()
        self.wait()
