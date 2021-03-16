import cv2

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMdiSubWindow, QLabel
from PyQt5.QtGui import QPixmap

from main_window_ui import MainWindowUI
from image import Image


class MainWindow(QtWidgets.QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui(self)

        self.action_open.triggered.connect(self.open_image)
        self.images = []

    def __browse_file(self):
        file_path = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;"
                                                                       "Image files (*.jpg, *.png, *.tif, *.gif);;"
                                                                       "Bitmap (*.bmp)")
        return file_path[0]

    def open_image(self):
        file_path = self.__browse_file()

        if not file_path:
            return

        img = cv2.imread(file_path, -1)

        sub_window = QMdiSubWindow()
        image_label = QLabel()

        pixmap = QPixmap(file_path)
        image_label.setPixmap(pixmap)
        sub_window.resize(pixmap.width() + 15, pixmap.height() + 35)

        sub_window.setWidget(image_label)
        sub_window.setWindowTitle(file_path.split("/")[-1])

        self.images.append(Image(img, sub_window))
        self.central_mdi_area.addSubWindow(sub_window)
        sub_window.show()


app = QtWidgets.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
