from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class StartUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.initUI()

    def initUI(self):
        selectDir = QPushButton('분류할 이미지 폴더 선택하기')
        selectDir.clicked.connect(self.p.selectDir)

        useSubDir = QCheckBox('하위 폴더 사용하기', self)
        useSubDir.setChecked(self.p.useSubDir)
        useSubDir.stateChanged.connect(self.useSubDir)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addWidget(selectDir)
        vBox.addWidget(useSubDir)
        vBox.addStretch(1)

        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addLayout(vBox)
        hBox.addStretch(1)

        self.setLayout(hBox)

    def useSubDir(self, x):
        self.p.useSubDir = x == Qt.Checked