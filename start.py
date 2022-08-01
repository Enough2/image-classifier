import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from classify import ClassifyUI
from dialog import EditDialog

class StartUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.initUI()

    def initUI(self):
        self.dirBtn = QPushButton('분류할 이미지 폴더 선택하기')
        self.dirBtn.clicked.connect(self.selectDir)

        self.subDirBtn = QCheckBox('하위 폴더 사용하기', self)
        self.subDirBtn.setChecked(self.p.useSubDir)
        self.subDirBtn.stateChanged.connect(self.useSubDir)

        self.dirName = QLabel('폴더명:')

        self.editBtn = QPushButton('분류 수정')
        self.editBtn.clicked.connect(self.classEdit)
        self.editBtn.setDisabled(True)

        self.saveBtn = QPushButton('저장할 파일 선택하기')
        self.saveBtn.clicked.connect(self.selectSave)
        self.saveBtn.setDisabled(True)

        self.saveName = QLabel('파일명:')
        self.saveName.setDisabled(True)

        self.startBtn = QPushButton('분류 시작')
        self.startBtn.clicked.connect(lambda _: self.p.changeScene(ClassifyUI))
        self.startBtn.setDisabled(True)

        vBox = QVBoxLayout()
        vBox.addStretch(10)
        vBox.addWidget(self.dirBtn)
        vBox.addWidget(self.subDirBtn)
        vBox.addWidget(self.dirName)
        vBox.addStretch(1)
        vBox.addWidget(self.editBtn)
        vBox.addStretch(1)
        vBox.addWidget(self.saveBtn)
        vBox.addWidget(self.saveName)
        vBox.addStretch(1)
        vBox.addWidget(self.startBtn)
        vBox.addStretch(10)

        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addLayout(vBox)
        hBox.addStretch(1)

        self.setLayout(hBox)

    def useSubDir(self, x):
        self.p.useSubDir = x == Qt.Checked

    def selectDir(self):
        dir = QFileDialog.getExistingDirectory(self, '분류할 이미지 폴더 선택하기')
        if dir:
            self.p.dir = dir
            self.dirName.setText(f"폴더명: {self.p.dir}")
            self.editBtn.setDisabled(False)
    
    def classEdit(self):
        dialog = EditDialog(self.p)
        if dialog.exec():
            lines = dialog.text.toPlainText().split("\n")
            self.p.labels = [line for line in lines]
            self.saveBtn.setDisabled(False)
            self.saveName.setDisabled(False)

    def selectSave(self):
        save = QFileDialog.getSaveFileName(self, '저장할 파일 선택하기', '', 'JSON 파일(*.json)')
        if save[0]:
            self.p.save = save[0]
            with open(self.p.save, 'w', encoding='utf-8') as file:
                json.dump(self.p.data, file, ensure_ascii=False)
            self.saveName.setText(f"파일명: {self.p.save}")
            self.startBtn.setDisabled(False)
