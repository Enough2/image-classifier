import os
import glob
from PyQt5.QtWidgets import *

class ClassifyUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.p = parent
        self.initUI()

    def initUI(self):
        self.p.statusBar().showMessage('파일 불러오는 중...')
        progressBar = QProgressBar()
        self.p.statusBar().addPermanentWidget(progressBar)
        progressBar.setRange(0, 0)

        for ext in self.p.exts:
            self.p.v['images'] += glob.glob(os.path.join(self.p.v['dir'], '*.' + ext))
            if self.p.v['useSubDir']:
                self.p.v['images'] += glob.glob(os.path.join(self.p.v['dir'], '**/*.' + ext))

            self.p.statusBar().showMessage(f"파일 불러오는 중... ({len(self.p.v['images']):,}개)")
        

    def selectDir(self):
        dir = QFileDialog.getExistingDirectory(self, '분류할 이미지 폴더 선택하기', './')
        self.p.v['dir'] = dir
