import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal

class ClassifyUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.initUI()

    def initUI(self):
        selectDir = QAction(QIcon('icons/folders.png'), '분류할 이미지 폴더 선택하기', self)
        selectDir.triggered.connect(self.p.selectDir)
        exitAction = QAction(QIcon('icons/logout.png'), '종료', self)
        exitAction.triggered.connect(self.p.close)

        self.p.toolBar = self.p.addToolBar('툴바')
        self.p.toolBar.addAction(selectDir)
        self.p.toolBar.addAction(exitAction)

        self.p.progressBar = QProgressBar()
        self.p.statusBar().addPermanentWidget(self.p.progressBar)

        self.p.thread = ImportThread(self.p)
        self.p.thread.update.connect(lambda x: self.p.statusBar().showMessage(f"파일 불러오는 중... ({x:,}개)"))
        self.p.thread.finish.connect(lambda x: self.p.statusBar().showMessage(f"파일 불러오기 완료 ({len(self.p.v['images']):,}개)") if x else None)
        self.p.thread.start()


class ImportThread(QThread):
    update = pyqtSignal(int)
    finish = pyqtSignal(bool)

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
        self.finish.emit(True)
        self.p.progressBar.setRange(0, len(images))
        self.p.progressBar.setValue(0)

    def stop(self):
        self.terminate()
        self.wait()
