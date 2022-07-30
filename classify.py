import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, QSize, pyqtSignal

from dialog import EditDialog

class ClassifyUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.groups = {}
        self.imageIdx = 0
        self.initUI()

    def initUI(self):
        self.p.progressBar = QProgressBar()
        self.p.statusBar().addPermanentWidget(self.p.progressBar)

        self.createToolBar()
        self.createLayout()

        self.p.thread = ImportThread(self.p)
        self.p.thread.update.connect(lambda x: self.addImage(x))
        self.p.thread.finished.connect(lambda x: self.loadImages() if x else None)
        self.p.thread.start()

    def createToolBar(self):
        self.p.toolBar = self.p.addToolBar('툴바')

        selectDir = QAction(QIcon('icons/folders.png'), '분류할 이미지 폴더 선택하기', self)
        selectDir.triggered.connect(self.p.selectDir)
        self.p.toolBar.addAction(selectDir)

        undoAction = QAction(QIcon('icons/arrow-back-up.png'), '취소', self)
        self.p.toolBar.addAction(undoAction)

        redoAction = QAction(QIcon('icons/arrow-forward-up.png'), '다시 실행', self)
        self.p.toolBar.addAction(redoAction)

        editAction = QAction(QIcon('icons/edit.png'), '분류 수정', self)
        editAction.triggered.connect(self.classEdit)
        self.p.toolBar.addAction(editAction)

        exitAction = QAction(QIcon('icons/logout.png'), '종료', self)
        exitAction.triggered.connect(self.p.close)
        self.p.toolBar.addAction(exitAction)

    def classEdit(self):
        dialog = EditDialog(self.p)
        if dialog.exec():
            lines = dialog.text.toPlainText().split("\n")
            self.p.labels = [line for line in lines]
            for i in range(15):
                if i < len(self.p.labels) and self.p.labels[i]:
                    text = self.p.labels[i][:10]
                else:
                    text = "미분류"
                self.p.classButtons[i].setText(f"{i:02} ({text})")

    def classify(self, idx):
        print(self.p.images[self.imageIdx], idx)

    def createLayout(self):
        grid = QGridLayout()

        self.groups['preview'] = QGroupBox('미리보기')
        self.groups['preview'].setFixedWidth(self.groups['preview'].height())
        fileNameBox = QHBoxLayout()
        self.fileName = QLineEdit()
        fileNameBox.addWidget(QLabel("파일명:"))
        fileNameBox.addWidget(self.fileName)
        self.fileName.setReadOnly(True)
        self.imageInfo = QLabel("너비: 0px, 높이: 0px")
        self.image = QLabel()
        self.image.setPixmap(QPixmap(""))
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vBox = QVBoxLayout()
        vBox.addLayout(fileNameBox)
        vBox.addWidget(self.imageInfo)
        vBox.addWidget(self.image)
        self.groups['preview'].setLayout(vBox)
        grid.addWidget(self.groups['preview'], 0, 0)

        self.groups['classify'] = QGroupBox('분류')
        vBox = QVBoxLayout()
        self.p.classButtons = []
        for i in range(15):
            button = QPushButton(f"{i:02} (미분류)")
            button.clicked.connect(lambda _, x = i: self.classify(x))
            self.p.classButtons.append(button)
            vBox.addWidget(self.p.classButtons[i])
        self.groups['classify'].setLayout(vBox)
        grid.addWidget(self.groups['classify'], 0, 1)

        self.groups['file'] = QGroupBox('파일')
        vBox = QVBoxLayout()
        self.fileList = QListWidget(self.groups['file'])
        vBox.addWidget(self.fileList)
        self.groups['file'].setLayout(vBox)
        grid.addWidget(self.groups['file'], 0, 2)

        self.setLayout(grid)

    def loadImages(self):
        self.p.thread.stop()
        self.p.statusBar().showMessage(f"파일 불러오기 완료 ({len(self.p.images):,}개)")
        pixmap = QPixmap(self.p.images[self.imageIdx])
        self.fileName.setText(self.p.images[self.imageIdx])
        self.imageInfo.setText(f"너비: {pixmap.width():,}px, 높이: {pixmap.height():,}px")
        pixmap = pixmap.scaled(self.image.width(), self.image.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image.setPixmap(pixmap)

    def addImage(self, path):
        if not path:
            self.p.statusBar().showMessage("파일 불러오는 중... (0개)")
            return

        self.p.images.append(path)
        self.p.statusBar().showMessage(f"파일 불러오는 중... ({len(self.p.images):,}개)")

class ImportThread(QThread):
    update = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent

    def run(self):
        self.p.progressBar.setRange(0, 0)
        self.p.progressBar.setValue(0)
        self.update.emit("")

        if self.p.useSubDir:
            for root, dirs, files in os.walk(self.p.dir):
                for file in files:
                    if file.split('.')[-1] in self.p.exts:
                        self.update.emit(os.path.join(root, file))
        else:
            for file in os.listdir(self.p.dir):
                if file.split('.')[-1] in self.p.exts:
                    self.update.emit(os.path.join(self.p.dir, file))

        self.p.progressBar.hide()
        self.finished.emit(True)

    def stop(self):
        self.terminate()
        self.wait()
