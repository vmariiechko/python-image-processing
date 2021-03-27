from cv2 import imread
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from main_window_ui import MainWindowUI
from image import Image


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui(self)

        self.action_open.triggered.connect(self.open_image)
        self.action_histogram.triggered.connect(self.show_histogram)
        self.action_profile.triggered.connect(self.show_intensity_profile)

        self.images = dict()

    def __browse_file(self):
        file_path = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;"
                                                                       "Image files (*.jpg, *.png, *.tif, *.gif);;"
                                                                       "Bitmap (*.bmp)")
        return file_path[0]

    def __get_selected_image(self):
        img_window = self.central_mdi_area.activeSubWindow()

        if not img_window:
            QMessageBox.warning(self, "Window isn't selected", "Please, select an image window")
            return None

        image = self.images.get(img_window)

        if not image:
            QMessageBox.warning(self, "Isn't image", "Please, select an image window")
            return None

        return image

    def open_image(self):
        file_path = self.__browse_file()

        if not file_path:
            return

        img_data = imread(file_path, -1)
        image = Image(img_data, file_path)

        self.images[image.img_window] = image
        self.central_mdi_area.addSubWindow(image.img_window)
        image.img_window.show()

    def show_histogram(self):
        image = self.__get_selected_image()

        if not image:
            return

        image.create_hist_window()

        self.central_mdi_area.addSubWindow(image.histogram_graphical)
        self.central_mdi_area.addSubWindow(image.histogram_graphical.histogram_list)
        image.histogram_graphical.show()

    def show_intensity_profile(self):
        image = self.__get_selected_image()

        if not image:
            return

        image.img_window.create_profile()

        self.central_mdi_area.addSubWindow(image.img_window.intensity_profile)
        image.img_window.intensity_profile.show()


app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
