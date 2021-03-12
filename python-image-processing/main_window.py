from PyQt5 import QtWidgets

from main_window_ui import MainWindowUI


class MainWindow(QtWidgets.QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(self)


app = QtWidgets.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
