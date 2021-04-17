from cv2 import imread
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

from main_ui import MainWindowUI
from image import Image, ImageBmp


class MainWindow(QMainWindow, MainWindowUI):
    """The MainWindow class represents the main window and its behavior."""

    def __init__(self, parent=None):
        """Create a new main window."""

        super().__init__(parent)
        self.init_ui(self)
        self.setAcceptDrops(True)

        self.action_open.triggered.connect(self.open_image)
        self.action_histogram.triggered.connect(self.show_histogram)
        self.action_profile.triggered.connect(self.show_intensity_profile)
        self.action_normalize.triggered.connect(lambda: self.run_histogram_operation("normalization"))
        self.action_equalize.triggered.connect(lambda: self.run_histogram_operation("equalization"))
        self.action_negation.triggered.connect(lambda: self.run_point_operation("negation"))
        self.action_threshold.triggered.connect(lambda: self.run_point_operation("threshold"))
        self.action_posterize.triggered.connect(lambda: self.run_point_operation("posterize"))
        self.action_smooth.triggered.connect(lambda: self.run_local_operation("smooth"))
        self.action_edge_dt_dir.triggered.connect(lambda: self.run_local_operation("edge_dt_dir"))
        self.action_edge_dt_nondir.triggered.connect(lambda: self.run_local_operation("edge_dt_nondir"))
        self.action_sharpen.triggered.connect(lambda: self.run_local_operation("sharpen"))

        self.images = dict()

    def __browse_file(self):
        """
        Navigate to the file using a file dialog.

        :return: The path to the chosen file
        :rtype: str
        """

        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;"
                                                                          "Image files (*.jpg, *.png, *.tif);;"
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

    def open_image(self, file_path=None):
        """Create :class:`image.Image` object of chosen image and show it in the sub-window."""

        if not file_path:
            file_path = self.__browse_file()

            if not file_path:
                return

        if file_path.split(".")[-1] == "bmp":
            with open(file_path, "rb") as file:
                try:
                    img_bmp = ImageBmp(file.read())
                    img_data = img_bmp.pixels
                except AssertionError:
                    img_data = imread(file_path, -1)
        else:
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

        if image.color_depth > 256:
            QMessageBox.warning(self, "Too high", "The size of the image item is too high.\n"
                                                  "Convert the image to 8 bits per pixel.")
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

        if not image.is_grayscale() or image.color_depth > 256:
            QMessageBox.warning(self, "Doesn't fit", "Selected image doesn't meet the requirements.\n"
                                                     "The image must be grayscale, 8 bits per pixel")
            return

        if operation == "normalization":
            image.normalize_histogram()
        elif operation == "equalization":
            image.equalize_histogram()

        image.update()

    def run_point_operation(self, operation):
        """
        Execute specified point operation.

        :param operation: The point operation, can be "negation", "threshold", "posterize"
        :type operation: str
        """

        image = self.__get_selected_image()

        if not image:
            return

        if operation == "negation":
            image.negation()
        elif operation == "threshold":

            if not image.is_grayscale():
                QMessageBox.warning(self, "Isn't grayscale", "Selected image has more than one channel.\n"
                                                             "Please, select a grayscale image.")
                return

            image.threshold()
        elif operation == "posterize":

            if not image.is_grayscale():
                QMessageBox.warning(self, "Isn't grayscale", "Selected image has more than one channel.\n"
                                                             "Please, select a grayscale image.")
                return

            image.posterize()

        image.update()

    def run_local_operation(self, operation):
        """
        Execute specified local operation.

        :param operation: The local operation, can be "smooth", "edge_dt"
        :type operation: str
        """

        image = self.__get_selected_image()

        if not image:
            return

        if operation == "smooth":
            image.smooth()
        elif operation == "edge_dt_dir":
            image.detect_edges(is_directional=True)
        elif operation == "edge_dt_nondir":
            image.detect_edges(is_directional=False)
        elif operation == "sharpen":
            image.sharpen()

        image.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.open_image(file_path)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
