import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.v = {'useSubDir': True, 'dir': ''}
        self.initUI()

    def initUI(self):
        selectDir = QPushButton('분류할 이미지 폴더 선택하기')
        selectDir.clicked.connect(self.selectDir)

        useSubDir = QCheckBox('하위 폴더 사용하기', self)
        useSubDir.setChecked(self.v['useSubDir'])
        useSubDir.stateChanged.connect(lambda x: self.state('useSubDir', x))

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

        self.setWindowTitle('image-classifier')
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

    def selectDir(self):
        dir = QFileDialog.getExistingDirectory(self, '분류할 이미지 폴더 선택하기', './')
        self.v['dir'] = dir


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
