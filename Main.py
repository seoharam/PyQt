import sys
from PyQt5.QtGui import QIcon
from Visualization import WindowClass
from PyQt5.QtWidgets import QApplication, QStyleFactory

# run
if __name__ == "__main__":                                                                                  # 특정 파이썬 파일이 직접 실행된 것인지 또는 다른 파이썬 파일에서 import된 것인지를 확인하는 용도 -> import 된 것이면 아래 명령어들이 실행 되지 않음
    app = QApplication(sys.argv)                                                                            # QApplication 클래스를 쓰기 위해 인스턴스를 생성하고, sys.argv를 통해 현재 소스코드에 대한 절대 경로를 전달 => 프로그램 실행 클래스
    mainWindow = WindowClass()                                                                              # 새로 정의한 WindowClass 클래스를 실행하기 위한 인스턴스 생성
    mainWindow.setWindowIcon(QIcon("./reference/schoolmark.png"))                                           # window의 아이콘을 설정하는 역할
    mainWindow.show()                                                                                       # window의 GUI를 화면에 보여주는 역할
    app.setStyle(QStyleFactory.create('Fusion'))                                                            
    app.exec_()                                                                                             # 무한루프를 돌게 하므로써 Ui를 화면에 계속 출력되게 만들어 준다. => 프로그램을 이벤트루프로 진입시키는 코드