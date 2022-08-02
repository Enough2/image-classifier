import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, QSize, pyqtSignal

from dialog import EditDialog

class ClassifyUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.p.images = []
        self.p.classButtons = []
        self.p.tabs = []
        self.p.data = [[] for _ in range(15)]
        self.p.undoRecord = []
        self.p.redoRecord = []
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
        selectDir.triggered.connect(self.selectDir)
        self.p.toolBar.addAction(selectDir)

        self.undoAction = QAction(QIcon('icons/arrow-back-up.png'), '취소', self)
        self.undoAction.triggered.connect(self.undo)
        self.undoAction.setDisabled(True)
        self.p.toolBar.addAction(self.undoAction)

        self.redoAction = QAction(QIcon('icons/arrow-forward-up.png'), '다시 실행', self)
        self.redoAction.triggered.connect(self.redo)
        self.redoAction.setDisabled(True)
        self.p.toolBar.addAction(self.redoAction)

        editAction = QAction(QIcon('icons/edit.png'), '분류 수정', self)
        editAction.triggered.connect(self.classEdit)
        self.p.toolBar.addAction(editAction)

        saveAction = QAction(QIcon('icons/download.png'), '저장할 파일 선택하기', self)
        saveAction.triggered.connect(self.selectSave)
        self.p.toolBar.addAction(saveAction)

        exitAction = QAction(QIcon('icons/logout.png'), '종료', self)
        exitAction.triggered.connect(self.p.close)
        self.p.toolBar.addAction(exitAction)

    def selectDir(self):
        dir = QFileDialog.getExistingDirectory(self, '분류할 이미지 폴더 선택하기')
        if dir:
            self.p.dir = dir
            if self.p.thread:
                self.p.thread.stop()
            self.p.changeScene(ClassifyUI)

    def undo(self):
        if self.imageIdx > 0 and self.p.undoRecord:
            idx = self.p.undoRecord.pop()
            if len(self.p.undoRecord) == 0:
                self.undoAction.setDisabled(True)
            self.p.redoRecord.append(idx)
            self.redoAction.setDisabled(False)
            self.imageIdx -= 1
            self.displayImage(self.imageIdx)
            self.p.data[idx].pop()
            self.p.tabs[idx].takeChild(self.p.tabs[idx].childCount() - 1)
            self.p.statusBar().showMessage(f"분류 ({self.imageIdx:,}/{len(self.p.images):,}개)")
            with open(self.p.save, 'w', encoding='utf-8') as file:
                json.dump(self.p.data, file, ensure_ascii=False)

    def redo(self):
        if self.p.redoRecord:
            idx = self.p.redoRecord.pop()
            if len(self.p.redoRecord) == 0:
                self.redoAction.setDisabled(True)
            self.p.undoRecord.append(idx)
            self.classify(idx)

    def classEdit(self):
        dialog = EditDialog(self.p)
        if dialog.exec():
            lines = dialog.text.toPlainText().split("\n")
            self.p.labels = [line for line in lines]
            for i in range(15):
                if i < len(self.p.labels) and self.p.labels[i]:
                    self.p.classButtons[i].setText(f"{i:02} ({self.p.labels[i][:10]})")
                    self.p.tabs[i].setText(0, f"{i:02} ({self.p.labels[i][:10]})")
                else:
                    self.p.classButtons[i].setText(f"{i:02} (미분류)")
                    self.p.tabs[i].setText(0, f"{i:02} (미분류)")

    def selectSave(self):
        save = QFileDialog.getSaveFileName(self, '저장할 파일 선택하기', '', 'JSON 파일(*.json)')
        if save[0]:
            self.p.save = save[0]
            with open(self.p.save, 'w', encoding='utf-8') as file:
                json.dump(self.p.data, file, ensure_ascii=False)
            self.saveName.setText(self.p.save)

    def classify(self, idx):
        self.p.data[idx].append(self.p.images[self.imageIdx])
        QTreeWidgetItem(self.p.tabs[idx], [self.p.images[self.imageIdx]])
        with open(self.p.save, 'w', encoding='utf-8') as file:
            json.dump(self.p.data, file, ensure_ascii=False)

        self.imageIdx += 1
        self.displayImage(self.imageIdx)
        self.p.undoRecord.append(idx) 
        self.undoAction.setDisabled(False)
        self.p.statusBar().showMessage(f"분류 ({self.imageIdx:,}/{len(self.p.images):,}개)")

    def createLayout(self):
        grid = QGridLayout()

        self.groups['preview'] = QGroupBox('미리보기')
        self.groups['preview'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        fileVBox = QHBoxLayout()
        self.fileName = QLineEdit()
        self.fileName.setReadOnly(True)
        self.fileName.setCursor(Qt.IBeamCursor)
        fileVBox.addWidget(QLabel("파일명:"))
        fileVBox.addWidget(self.fileName)

        self.imageInfo = QLabel("너비: 0px, 높이: 0px")
        self.image = QLabel()
        self.image.setPixmap(QPixmap(""))
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        vBox = QVBoxLayout()
        vBox.addLayout(fileVBox)
        vBox.addWidget(self.imageInfo)
        vBox.addWidget(self.image)
        self.groups['preview'].setLayout(vBox)
        grid.addWidget(self.groups['preview'], 0, 0)


        self.groups['classify'] = QGroupBox('분류')
        vBox = QVBoxLayout()
        self.p.classButtons = []
        for i in range(15):
            if i < len(self.p.labels) and self.p.labels[i]:
                button = QPushButton(f"{i:02} ({self.p.labels[i][:10]})")
            else:
                button = QPushButton(f"{i:02} (미분류)")
            button.clicked.connect(lambda _, x = i: self.classify(x))
            self.p.classButtons.append(button)
            vBox.addWidget(self.p.classButtons[i])
        self.groups['classify'].setLayout(vBox)
        grid.addWidget(self.groups['classify'], 0, 1)

    
        self.groups['file'] = QGroupBox('파일')

        dirVBox = QHBoxLayout()
        self.dirName = QLineEdit()
        self.dirName.setReadOnly(True)
        self.dirName.setCursor(Qt.IBeamCursor)
        self.dirName.setText(self.p.dir)
        dirVBox.addWidget(QLabel("폴더명:"))
        dirVBox.addWidget(self.dirName)

        saveVBox = QHBoxLayout()
        self.saveName = QLineEdit()
        self.saveName.setReadOnly(True)
        self.saveName.setCursor(Qt.IBeamCursor)
        self.saveName.setText(self.p.save)
        saveVBox.addWidget(QLabel("파일명:"))
        saveVBox.addWidget(self.saveName)

        self.p.fileTree = QTreeWidget()
        self.p.fileTree.setHeaderLabels(['파일명'])
        for i in range(15):
            if i < len(self.p.labels) and self.p.labels[i]:
                self.p.tabs.append(QTreeWidgetItem([f"{i:02} ({self.p.labels[i][:10]})"]))
            else:
                self.p.tabs.append(QTreeWidgetItem([f"{i:02} (미분류)"]))
            self.p.fileTree.addTopLevelItem(self.p.tabs[i])
        
        vBox = QVBoxLayout()
        vBox.addLayout(dirVBox)
        vBox.addLayout(saveVBox)
        vBox.addWidget(self.p.fileTree)
        self.groups['file'].setLayout(vBox)
        grid.addWidget(self.groups['file'], 0, 2)

        self.setLayout(grid)

    def displayImage(self, idx):
        pixmap = QPixmap(self.p.images[idx])
        self.fileName.setText(self.p.images[idx])
        self.imageInfo.setText(f"너비: {pixmap.width():,}px, 높이: {pixmap.height():,}px")
        pixmap = pixmap.scaled(self.image.width(), self.image.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image.setPixmap(pixmap)

    def loadImages(self):
        self.p.thread.stop()
        self.p.statusBar().showMessage(f"파일 불러오기 완료 ({len(self.p.images):,}개)")
        self.displayImage(self.imageIdx)

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
