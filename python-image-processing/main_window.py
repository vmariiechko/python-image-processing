from cv2 import imread
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from main_window_ui import MainWindowUI
from image import Image


class MainWindow(QMainWindow, MainWindowUI):
    """The MainWindow class represents the main window and its behavior."""

    def __init__(self, parent=None):
        """Create a new main window."""

        super().__init__(parent)
        self.init_ui(self)

        self.action_open.triggered.connect(self.open_image)
        self.action_histogram.triggered.connect(self.show_histogram)
        self.action_profile.triggered.connect(self.show_intensity_profile)
        self.action_normalize.triggered.connect(lambda: self.run_histogram_operation("normalization"))
        self.action_equalize.triggered.connect(lambda: self.run_histogram_operation("equalization"))

        self.images = dict()

    def __browse_file(self):
        """
        Navigate to the file using a file dialog.

        :return: The path to the chosen file
        :rtype: str
        """

        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;"
                                                                          "Image files (*.jpg, *.png, *.tif, *.gif);;"
                                                                          "Bitmap (*.bmp)")
        return file_path

    def __get_selected_image(self):
        """
        Find an active image window.

        If there's no window selected or the active window isn't an image,
        then show a warning message window.

        :return: The :class:`image.Image` object of selected window
        :rtype: :class:`image.Image`
        """

        img_window = self.central_mdi_area.activeSubWindow()

        if not img_window:
            QMessageBox.warning(self, "Window isn't selected", "Please, select an image window.")
            return None

        image = self.images.get(img_window)

        if not image:
            QMessageBox.warning(self, "Isn't image", "Please, select an image window.")
            return None

        return image

    def open_image(self):
        """Create :class:`image.Image` object of chosen image and show it in the sub-window."""

        file_path = self.__browse_file()

        if not file_path:
            return

        img_data = imread(file_path, -1)
        image = Image(img_data, file_path)

        self.images[image.img_window] = image
        self.central_mdi_area.addSubWindow(image.img_window)
        image.img_window.show()

    def show_histogram(self):
        """Create a graphical representation of the histogram and show it in the sub-window."""

        image = self.__get_selected_image()

        if not image:
            return

        image.create_hist_window()

        self.central_mdi_area.addSubWindow(image.histogram_graphical)
        self.central_mdi_area.addSubWindow(image.histogram_graphical.histogram_list)
        image.histogram_graphical.show()

    def show_intensity_profile(self):
        """Create intensity profile of drawn line and show it in the sub-window."""

        image = self.__get_selected_image()

        if not image:
            return

        image.img_window.create_profile()

        self.central_mdi_area.addSubWindow(image.img_window.intensity_profile)
        image.img_window.intensity_profile.show()

    def run_histogram_operation(self, operation):
        """
        Execute specified histogram operation.

        :param operation: The histogram operation, can be "normalization" or "equalization"
        :type operation: str
        """

        image = self.__get_selected_image()

        if not image:
            return

        if not image.is_grayscale():
            QMessageBox.warning(self, "Not grayscale", "Selected image isn't grayscale.")
            return

        if operation == "normalization":
            image.normalize_histogram()
        elif operation == "equalization":
            image.equalize_histogram()

        image.update()


app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
