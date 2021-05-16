from functools import wraps

from cv2 import imread, imwrite
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

from main_ui import MainWindowUI
from image import Image, ImageWindow, ImageBmp


def validate_active_image(method):
    """The decorator to validate the active image to be not `None`."""

    @wraps(method)
    def wrapper(self, *args):
        if not self.active_image:
            QMessageBox.warning(self, "There is no uploaded image", "Please, open an image using\n"
                                                                    "'File->Open' or drag & drop action.")
            return
        method(self, *args)
    return wrapper


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
        self.action_cascade.triggered.connect(self.central_mdi_area.cascadeSubWindows)
        self.action_exit.triggered.connect(self.close)

        # Image menu actions
        self.action_rename.triggered.connect(self.rename_title)
        self.action_duplicate.triggered.connect(self.duplicate)
        self.group_image_type.triggered.connect(self.set_image_type)

        # Analyze menu actions
        self.action_histogram.triggered.connect(self.show_histogram)
        self.action_profile.triggered.connect(self.show_intensity_profile)

        # Operation menu actions
        self.action_normalize.triggered.connect(lambda: self.run_operation("normalize"))
        self.action_equalize.triggered.connect(lambda: self.run_operation("equalize"))
        self.action_negation.triggered.connect(lambda: self.run_operation("negation"))
        self.action_posterize.triggered.connect(lambda: self.run_operation("posterize"))
        self.action_smooth.triggered.connect(lambda: self.run_operation("smooth"))
        self.action_edge_dt_nondir.triggered.connect(lambda: self.run_operation("edge_dt"))
        self.action_edge_dt_dir.triggered.connect(lambda: self.run_operation("edge_dt_dir"))
        self.action_sharpen.triggered.connect(lambda: self.run_operation("sharpen"))
        self.action_convolve.triggered.connect(lambda: self.run_operation("convolve"))
        self.action_gray_morphology.triggered.connect(lambda: self.run_operation("morphology"))
        self.action_image_calculator.triggered.connect(self.image_calculator)
        self.action_threshold.triggered.connect(lambda: self.run_operation("threshold"))
        self.action_watershed.triggered.connect(lambda: self.run_operation("watershed"))

        self.central_mdi_area.subWindowActivated.connect(self.__update_active_image)

        self.images = dict()
        self.active_image = None

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

    def __update_active_image(self, sub_window):
        """
        Find a selected image and set it as active.

        :param sub_window: The active sub-window, the sender of the signal
        """

        if isinstance(sub_window, ImageWindow):
            self.active_image = self.images.get(sub_window)
            self.set_image_type(None)

    def __activate_last_image(self):
        """Change activated image to the last uploaded."""

        try:
            self.active_image = list(self.images.values())[-1]
            self.set_image_type(None)
        except IndexError:
            self.active_image = None

    def __remove_image(self, image):
        """
        Remove closed image from :attr:`images`.

        :param image: The image to remove
        :type image: :class:`image.Image`
        """

        self.images = {window: img for window, img in self.images.items() if img != image}
        self.__activate_last_image()

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

    @validate_active_image
    def save_image(self, *args):
        """Save the file using a file dialog."""

        file_path, _ = QFileDialog.getSaveFileName(self, "Save file", self.active_image.img_name,
                                                   "All Files (*);;"
                                                   "Bitmap (*.bmp *.dib);;"
                                                   "Image files (*.jpg *.png *.tif)")

        if not file_path:
            return

        imwrite(file_path, self.active_image.img_data)

    @validate_active_image
    def rename_title(self, *args):
        """Change the image name and title."""

        self.active_image.rename()

    @validate_active_image
    def duplicate(self, *args):
        """Create the image duplicate."""

        image_copy = Image(self.active_image.img_data, "copy_" + self.active_image.img_name)
        image_copy.rename()
        self.__add_image_window(image_copy)

    @validate_active_image
    def set_image_type(self, action):
        """
        Set the image type for selected image.

        If :param:`action` is `None`,
        check action for the active current image type.
        Otherwise, set a specified image type.

        :param action: The action-sender with type text
        """

        is_grayscale = self.active_image.is_grayscale()

        if not action:
            actions = self.group_image_type.actions()
            if is_grayscale:
                actions[0].setChecked(True)
            else:
                actions[1].setChecked(True)
            return

        img_type = action.text()

        # Current and given image types are the same
        if (is_grayscale and img_type == "Grayscale") \
                or (not is_grayscale and img_type == "BGR-Color"):
            return

        self.active_image.change_type(img_type)
        self.active_image.update()

    @validate_active_image
    def show_histogram(self, *args):
        """Create a graphical representation of the histogram and show it in the sub-window."""

        if self.active_image.color_depth > 256:
            QMessageBox.warning(self, "Too high", "The size of the image item is too high.\n"
                                                  "Convert the image to 8 bits per pixel.")
            return

        self.active_image.create_hist_window()

        self.central_mdi_area.addSubWindow(self.active_image.histogram_graphical)
        self.central_mdi_area.addSubWindow(self.active_image.histogram_graphical.histogram_list)
        self.active_image.histogram_graphical.show()

    @validate_active_image
    def show_intensity_profile(self, *args):
        """Create intensity profile of drawn line and show it in the sub-window."""

        self.active_image.img_window.create_profile()

        self.central_mdi_area.addSubWindow(self.active_image.img_window.intensity_profile)
        self.active_image.img_window.intensity_profile.show()

    @validate_active_image
    def run_operation(self, operation):
        """
        Execute specified image operation.

        The operation can be "equalize", "negation" and other dialog
        operations defined in :attr:`image.Image.DIALOG_OPERATIONS`.

        :param operation: The operations to execute
        :type operation: str
        """

        is_colored = not self.active_image.is_grayscale()

        if operation == "watershed" and not is_colored:
            QMessageBox.warning(self, "Isn't colored", "Selected image has one channel.\n"
                                                       "Please, select a color image.")
            return

        if operation in ("threshold", "segmentation", "posterize") and is_colored:
            QMessageBox.warning(self, "Isn't grayscale", "Selected image has more than one channel.\n"
                                                         "Please, select a grayscale image.")
            return

        elif operation in ("normalize", "equalize", "morphology") \
                and (is_colored or self.active_image.color_depth > 256):
            QMessageBox.warning(self, "Doesn't fit", "Selected image doesn't meet the requirements.\n"
                                                     "The image must be grayscale, 8 bits per pixel.")
            return

        if operation == "equalize":
            self.active_image.equalize_histogram()
        elif operation == "negation":
            self.active_image.negation()
        else:
            self.active_image.run_dialog_operation(operation)

        self.active_image.update()

    @validate_active_image
    def image_calculator(self, *args):
        """Perform one of the double-argument point operations between two images."""

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
