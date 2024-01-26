import time
from PyQt5.QtCore import QThread, pyqtSignal

class Model(QThread):
    finished = pyqtSignal(object, object)
    progress = pyqtSignal(int, object)
        
    def __init__(self):
        super().__init__()


    def run(self):
        start = time.time()

        # region : run
        ########################################

        ########################################
        # endregion
        
        # 최종 시간 계산 및 도출
        finish = round(time.time() - start, 2)
        
        # progress bar value 시그널 발생
        self.progress.emit(100, f'{finish} [sec]')
        
        # array 도출 -> Thread로 작업이 완료되었음을 알리기 위해 사용되는 시그널을 발생
        self.finished.emit()                   