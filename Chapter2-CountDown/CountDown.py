import sys

from PyQt6.QtCore import Qt
from PySide6 import QtCore
from PySide6.QtWidgets import (QApplication,
                             QMainWindow, QWidget,
                             QVBoxLayout,QHBoxLayout, QLabel, QLineEdit,QListWidget,
                            QTextEdit,
                             QPushButton,QMessageBox,QListWidgetItem)

DURATION_INT = 60

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

class CountDownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)
        self.setGeometry(200, 200, 200, 200)
        self.setWindowTitle("Count Down App")
        self.create_widgets()
        self.setup_layout()


    def create_widgets(self):
        self.welcome_label = QLabel("Welcome to my App")
        self.welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.count_down_label = QLabel("01:00")
        self.count_down_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.count_down_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        # Buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.startTimer)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stopTimer)
        pass

    def setup_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.count_down_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        pass

    def startTimer(self):
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)
        self.myTimer.timeout.connect(self.timerTimeOut)
        self.myTimer.start(1000)

    def timerTimeOut(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.time_left_int = DURATION_INT
        self.update_gui()

    def update_gui(self):
        minsec = secs_to_minsec(self.time_left_int)
        self.count_down_label.setText(minsec)

    def stopTimer(self):
        self.myTimer.stop()
        self.count_down_label.setText("01:00")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CountDownApp()
    window.show()
    sys.exit(app.exec())

