import json
import traceback
import warnings
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

warnings.simplefilter(action = 'ignore', category = UserWarning)

from Model import Model
import pandas as pd

# UI파일과 python 코드 파일 연결 -> 상대 좌표이기 때문에 같은 directory(주소) 안에 위치 ----------------------------------------------------

form_class = uic.loadUiType("./reference/seoharam.ui")[0]                                                      # 2개의 튜플로 이뤄져있어, 0번째는 MainWindow, 1번째는 QtWidgets의 QMainWindow 클래스, 상대 경로는 같은 폴더 내에만 있으면 됨

# QMainWindow를 사용하기 위한 클래스 생성 => "기본 뼈대" ---------------------------------------------------------------------------------

class WindowClass(QMainWindow, form_class):                                                                    # 매개변수 자리에 form_class도 포함되어 있기때문에 해당 ui에 정의 되어 있던 속성이나 메서드를 모두 상속 받는다.
    def __init__(self):                                                                                        # 해당 클래스가 시작될때 가장 먼저 시작할 수 있도록 하는 함수
        super().__init__()                                                                                     # 부모클래스(QMainWindow)의 생성자(객체를 만들때 실행되는 함수)를 실행
        self.setupUi(self)                                                                                     # setupUi는 Qt designer를 통해 구성한 Ui를 화면에 출력 가능 => 코드를 통해서 ui 설정시 함수(def setupUi)를 만들어 사용
        self.statusBar.setStyleSheet("background-color: white; color: black;")                                 # 상태바 배경 색 및 글자 색 변경
        
        # region: 버튼 및 위젯 변수 확인
        ##############################################
        # 버튼
        self.pushButton_plot
        self.pushButton_export
        self.pushButton_run
        self.pushButton_input

        # line & text
        self.lineEdit_progressbar
        self.treeWidget_path_info

        # screen
        self.widget_plot

        # Layout
        self.horizontalLayout
        self.gridLayout_array
        self.formLayout_progressbar
        self.gridLayout_plot
        self.gridLayout_info
        self.gridLayout_layer

        # status bar
        self.statusBar

        # progress bar
        self.progressBar_array

        # combo box
        self.comboBox_plot
        ##############################################
        # endregion

        # region: 위젯 함수 연결
        ##############################################
        self.pushButton_input.clicked.connect(self.import_input_value)
        self.pushButton_run.clicked.connect(self.run_model)
        self.pushButton_plot.clicked.connect(self.show_grid_plot)
        self.pushButton_export.clicked.connect(self.export_kp_report)
        self.pushButton_plot.setEnabled(False)
        self.pushButton_run.setEnabled(False)
        self.pushButton_input.setEnabled(True)
        self.treeWidget_path_info.setColumnCount(2)                  # 두 개의 열을 가진 트리 위젯
        self.treeWidget_path_info.setHeaderLabels(["Key", "Value"])  # 열 제목 설정
        ##############################################
        # endregion

    def import_input_value(self):
        try:
            options = QFileDialog.Options()

            # 파일 선택
            self.file_path, _ = QFileDialog.getOpenFileName(self, "Open File", './reference/input/UserInput', "All Files (*.json)", options=options)

            # 사용자 데이터 읽기
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.user_data = json.load(file)

            # 해당 경로에 포함되는 json 파일을 불러오는 함수 실행
            self.run_model()

        except:
            traceback.print_exc()
            self.statusBar.showMessage("Please set node position again")
            pass

    def run_model(self):
        try:
            # 작업을 위한 객체 생성
            self.MakeData = Model(self.layer_name_list, self.start_node, self.finish_node, self.user_data, self.country) 
            
            # Thread를 이용한 작업 실행     
            self.MakeData.start()                                                                                             
            self.MakeData.finished.connect(self.complete_make_data)
            self.MakeData.progress.connect(self.update_progressbar)

        except:
            traceback.print_exc()
            pass

    def complete_model(self):
        # finished에 할당한 변수들 parameter로 넣기
        self.statusBar.showMessage("Finish Create Map input data")

        # 초기 출력 화면
        fig = fig
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, self)
        self.gridLayout_plot.addWidget(toolbar)
        self.gridLayout_plot.addWidget(canvas)

    def export_kp_report(self):
        # 결과물 엑셀 저장
        file_path = './reference/output/output.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            output = json.load(file)

        df = pd.DataFrame(output)
        df.to_excel('./reference/output/output.xlsx')
        self.pushButton_export.setEnabled(False)
        self.statusBar.showMessage("Finish exporting kp report")

    def update_progressbar(self, value, text):
        self.lineEdit_progressbar.setText(text)
        self.progressBar_array.setValue(value)

    def add_dict_to_tree(self, tree, path_data, parent_item=None):
        for key, value in path_data.items():
            item = QTreeWidgetItem(parent_item or tree)
            item.setText(0, str(key))
            if isinstance(value, dict):
                self.add_dict_to_tree(tree, value, item)
            else:
                item.setText(1, str(value))
            if not parent_item:
                tree.addTopLevelItem(item)

            # 각 항목의 배경색을 설정 (예: 홀수 행은 노란색, 짝수 행은 파란색)
            if tree.indexOfTopLevelItem(item) % 2 == 0:
                item.setBackground(0, QColor(212, 212, 212))  # 파란색
                item.setBackground(1, QColor(212, 212, 212))  # 파란색
            else:
                item.setBackground(0, QColor(255, 255, 255))  # 노란색
                item.setBackground(1, QColor(255, 255, 255))  # 노란색

    def show_grid_plot(self):
        while self.gridLayout_plot.count():
            item = self.gridLayout_plot.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.comboBox_plot.currentText() == 'LNDARE':
            channel = 'LNDARE'
            fig = fig
            canvas = FigureCanvas(fig)
            toolbar = NavigationToolbar(canvas, self)
            self.gridLayout_plot.addWidget(toolbar)
            self.gridLayout_plot.addWidget(canvas)