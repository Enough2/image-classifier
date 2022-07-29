from PyQt5.QtWidgets import *

class EditDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('분류 수정')
        self.setFixedSize(640, 360)

        vBox = QVBoxLayout()
        label = QLabel('분류에 사용될 식별자를 입력해주세요. (최대 15개, 0~14번)')
        hBox = QHBoxLayout()
        fileSelect = QPushButton("분류 텍스트 파일 선택하기")
        fileSelect.clicked.connect(self.selectFile)
        self.fileName = QLabel("파일명: 선택되지 않음")
        self.fileName.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        hBox.addWidget(fileSelect)
        hBox.addWidget(self.fileName)
        self.text = QTextEdit()
        vBox.addWidget(label)
        vBox.addLayout(hBox)
        vBox.addWidget(self.text)

        hBox = QHBoxLayout()
        clear = QPushButton("초기화")
        clear.clicked.connect(lambda: self.text.setText(""))
        confirm = QPushButton('확인')
        confirm.clicked.connect(lambda: self.done(1))
        cancel = QPushButton('취소')
        cancel.clicked.connect(lambda: self.done(0))
        hBox.addWidget(clear)
        hBox.addStretch(1)
        hBox.addWidget(confirm)
        hBox.addWidget(cancel)
        vBox.addLayout(hBox)

        self.setLayout(vBox)

    def selectFile(self):
        fileName = QFileDialog.getOpenFileName(self, '분류 텍스트 파일 선택하기') 
        if fileName[0]:
            with open(fileName[0], 'r', encoding='utf-8') as file:
                self.text.setText(''.join(file.readlines()))
                self.fileName.setText(f"파일명: {fileName[0]}")
        