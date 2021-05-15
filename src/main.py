from cv2 import imread, imwrite
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

from main_ui import MainWindowUI
from image import Image, ImageBmp


class MainWindow(QMainWindow, MainWindowUI):
    """The MainWindow class represents the main window and its behavior."""

    SUPPORTED_FILE_EXTENSIONS = ["bmp", "jpeg", "jpg", "png", "tiff", "tif"]

    def __init__(self, parent=None):
        """Create a new main window."""

        super().__init__(parent)
        self.init_ui(self)
        self.setAcceptDrops(True)

        # File menu actions
        self.action_open.triggered.connect(self.open_image)
        self.action_save.triggered.connect(self.save_image)
        self.action_exit.triggered.connect(self.close)

        # Image menu actions
        self.action_rename.triggered.connect(self.rename_title)
        self.action_duplicate.triggered.connect(self.duplicate)

        # Analyze menu actions
        self.action_histogram.triggered.connect(self.show_histogram)
        self.action_profile.triggered.connect(self.show_intensity_profile)

        # Operation menu actions
        self.action_normalize.triggered.connect(lambda: self.run_operation("normalize"))
        self.action_equalize.triggered.connect(lambda: self.run_operation("equalize"))
        self.action_negation.triggered.connect(lambda: self.run_operation("negation"))
        self.action_threshold.triggered.connect(lambda: self.run_operation("threshold"))
        self.action_posterize.triggered.connect(lambda: self.run_operation("posterize"))
        self.action_smooth.triggered.connect(lambda: self.run_operation("smooth"))
        self.action_edge_dt_nondir.triggered.connect(lambda: self.run_operation("edge_dt"))
        self.action_edge_dt_dir.triggered.connect(lambda: self.run_operation("edge_dt_dir"))
        self.action_sharpen.triggered.connect(lambda: self.run_operation("sharpen"))
        self.action_convolve.triggered.connect(lambda: self.run_operation("convolve"))
        self.action_gray_morphology.triggered.connect(lambda: self.run_operation("morphology"))
        self.action_image_calculator.triggered.connect(self.image_calculator)

        self.images = dict()

    def __browse_file(self):
        """
        Navigate to the file using a file dialog.

        :return: The path to the chosen file
        :rtype: str
        """

        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;"
                                                                          "Bitmap (*.bmp);;"
                                                                          "JPEG files (*.jpeg *.jpg);;"
                                                                          "Portable Network Graphics (*.png);;"
                                                                          "TIFF files (*.tiff *.tif);;"
                                                                          "Supported files (*.bmp *.jpeg *.jpg "
                                                                          "*.png *.tiff *.tif);;")
        return file_path

    def __add_image_window(self, image):
        """
        Add a new image to the sub-window.

        :param image: The image to add
        :type image: :class:`image.Image`
        """

        self.images[image.img_window] = image
        self.central_mdi_area.addSubWindow(image.img_window)
        image.img_window.closed.connect(lambda img=image: self.__remove_image(img))
        image.img_window.show()

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

    def __remove_image(self, image):
        """
        Remove closed image from :attr:`images`.

        :param image: The image to remove
        :type image: :class:`image.Image`
        """

        self.images = {window: img for window, img in self.images.items() if img != image}

    def open_image(self, file_path=None):
        """Create :class:`image.Image` object of chosen image and show it in the sub-window."""

        if not file_path:
            file_path = self.__browse_file()

            if not file_path:
                return

        file_extension = file_path.split(".")[-1]
        if file_extension not in self.SUPPORTED_FILE_EXTENSIONS:
            QMessageBox.warning(self, "Not supported extension", "The opened file has unsupported extension")
            return

        # Try to open .bmp image using own implementation
        if file_extension == "bmp":
            with open(file_path, "rb") as file:
                try:
                    img_bmp = ImageBmp(file.read())
                    img_data = img_bmp.pixels
                except AssertionError:
                    img_data = imread(file_path, -1)
        else:
            # Open image using opencv function
            img_data = imread(file_path, -1)

        img_name = file_path.split("/")[-1]
        image = Image(img_data, img_name)
        self.__add_image_window(image)

    def save_image(self):
        """Save the file using a file dialog."""

        image = self.__get_selected_image()

        if not image:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save file", image.img_name,
                                                   "All Files (*);;"
                                                   "Bitmap (*.bmp *.dib);;"
                                                   "Image files (*.jpg *.png *.tif)")

        if not file_path:
            return

        imwrite(file_path, image.img_data)

    def rename_title(self):
        """Change the image name and title."""

        image = self.__get_selected_image()

        if not image:
            return

        image.rename()

    def duplicate(self):
        """Create the image duplicate."""

        image = self.__get_selected_image()

        if not image:
            return

        image_copy = Image(image.img_data, "copy_" + image.img_name)
        image_copy.rename()
        self.__add_image_window(image_copy)

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

    def run_operation(self, operation):
        """
        Execute specified image operation.

        The operation can be "equalize", "negation" and other dialog
        operations defined in :attr:`image.Image.DIALOG_OPERATIONS`.

        :param operation: The operations to execute
        :type operation: str
        """

        image = self.__get_selected_image()

        if not image:
            return

        is_colored = not image.is_grayscale()

        if operation in ("segmentation", "posterize") and is_colored:
            QMessageBox.warning(self, "Isn't grayscale", "Selected image has more than one channel.\n"
                                                         "Please, select a grayscale image.")
            return

        elif operation in ("normalize", "equalize", "morphology") and (is_colored or image.color_depth > 256):
            QMessageBox.warning(self, "Doesn't fit", "Selected image doesn't meet the requirements.\n"
                                                     "The image must be grayscale, 8 bits per pixel.")
            return

        if operation == "equalize":
            image.equalize_histogram()
        elif operation == "negation":
            image.negation()
        else:
            image.run_dialog_operation(operation)

        image.update()

    def image_calculator(self):
        """Perform one of the double-argument point operations between two images."""

        if len(self.images) < 1:
            QMessageBox.warning(self, "There is no uploaded image", "Please, open an image using\n"
                                                                    "'File->Open' or drag & drop action.")
            return

        new_image = Image.calculator(self.images.values())

        if new_image:
            image = Image(*new_image)
            self.__add_image_window(image)

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
