from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from main_window_ui import MainWindowUI


class MainWindow(QtWidgets.QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui(self)

        self.action_open.triggered.connect(self.select_file)

    def select_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;(*.jpg, *.png, *.tif);;(*.bmp)")

        if file_name:
            print(file_name)


app = QtWidgets.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
