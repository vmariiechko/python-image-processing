from functools import wraps

from cv2 import imread, imwrite
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

from main_ui import MainWindowUI
from image import Image, ImageWindow, ImageBmp
from style_sheet import load_style_sheet


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
        self.action_open.triggered.connect(self.open_images)
        self.action_save.triggered.connect(self.save_image)
        self.action_cascade.triggered.connect(self.central_mdi_area.cascadeSubWindows)
        self.action_exit.triggered.connect(self.close)

        # Image menu actions
        self.action_rename.triggered.connect(self.rename_title)
        self.action_duplicate.triggered.connect(self.duplicate)
        self.action_image_info.triggered.connect(self.show_image_info)
        self.group_image_type.triggered.connect(self.set_image_type)
        self.action_color_depth_uint8.triggered.connect(self.set_color_depth)

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

    def __browse_files(self):
        """
        Navigate to the files using a file dialog.

        :return: The paths to the chosen files
        :rtype: list[str]
        """

        files_paths, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "All Files (*);;"
                                                                             "Bitmap (*.bmp);;"
                                                                             "JPEG files (*.jpeg *.jpg);;"
                                                                             "Portable Network Graphics (*.png);;"
                                                                             "TIFF files (*.tiff *.tif);;"
                                                                             "Supported files (*.bmp *.jpeg *.jpg "
                                                                             "*.png *.tiff *.tif);;")
        return files_paths

    def __add_image_window(self, image):
        """
        Add a new image to the sub-window.

        :param image: The image to add
        :type image: :class:`image.Image`
        """

        self.images[image.subwindow] = image
        self.central_mdi_area.addSubWindow(image.subwindow)
        image.subwindow.closed.connect(lambda img=image: self.__remove_image(img))
        image.subwindow.show()

    def __update_active_image(self, sub_window):
        """
        Find a selected image and set it as active.

        :param sub_window: The active sub-window, the sender of the signal
        """

        if isinstance(sub_window, ImageWindow):
            self.active_image = self.images.get(sub_window)
            self.set_image_type(None)
            self.set_color_depth(None)

    def __activate_last_image(self):
        """Change activated image to the last uploaded."""

        try:
            self.active_image = list(self.images.values())[-1]
            self.set_image_type(None)
            self.set_color_depth(None)
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

    def open_images(self, files_paths=None):
        """Open images by their paths."""

        if not files_paths:
            files_paths = self.__browse_files()

            if not files_paths:
                return

        for file_path in files_paths:
            self.open_image(file_path)

    def open_image(self, file_path):
        """Create :class:`image.Image` object of chosen image and show it in the sub-window."""

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

        file_path, _ = QFileDialog.getSaveFileName(self, "Save file", self.active_image.name,
                                                   "All Files (*);;"
                                                   "Bitmap (*.bmp *.dib);;"
                                                   "Image files (*.jpg *.png *.tif)")

        if not file_path:
            return

        imwrite(file_path, self.active_image.data)

    @validate_active_image
    def rename_title(self, *args):
        """Change the image name and title."""

        self.active_image.rename()

    @validate_active_image
    def duplicate(self, *args):
        """Create the image duplicate."""

        image_copy = Image(self.active_image.data, "copy_" + self.active_image.name)
        image_copy.rename()
        self.__add_image_window(image_copy)

    @validate_active_image
    def set_image_type(self, action):
        """
        Set the image type for the selected image.

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
        self.set_color_depth(None)
        self.active_image.update()

    @validate_active_image
    def set_color_depth(self, action):
        """
        Set the image color depth for the selected image.

        It's possible to change color depth only to
        8 bit per pixel from other bit lengths.

        If :param:`action` is `None`,
        check action for the active current image color depth.
        Otherwise, set an 8 bit per pixel color depth.

        :param action: The action-sender with color depth text
        """

        is_uint8 = self.active_image.data.dtype.itemsize == 1

        if not action:
            self.action_color_depth_uint8.setChecked(is_uint8)
            return

        if is_uint8:
            return
        else:
            self.active_image.change_color_depth_2_uint8()

    @validate_active_image
    def show_image_info(self, *args):
        """Show basic image information in the message box."""

        bits_per_pixel = str(8 * self.active_image.data.dtype.itemsize)
        bits_per_pixel += " (Grayscale)" if self.active_image.is_grayscale() else " (BGR)"
        data = self.active_image.data

        image_info = f"""
                        <table>
                            <tr><td>Title</td>          <td>{self.active_image.name}</td></tr>
                            <tr><td>Width</td>          <td>{data.shape[0]}</td></tr>
                            <tr><td>Height</td>         <td>{data.shape[1]}</td></tr>
                            <tr><td>Bits per pixel</td> <td>{bits_per_pixel}</td></tr>
                            <tr><td>Display range&nbsp;&nbsp;&nbsp;&nbsp;</td>
                                                        <td>0-{self.active_image.color_depth - 1}</td></tr>
                            <tr><td>Min Value</td>      <td>{data.min()}</td></tr>
                            <tr><td>Max Value</td>      <td>{data.max()}</td></tr>
                        </table>
                      """

        QMessageBox.information(self, "Image Information", image_info)

    @validate_active_image
    def show_histogram(self, *args):
        """Create a graphical representation of the histogram and show it in the sub-window."""

        if self.active_image.color_depth > 256:
            QMessageBox.warning(self, "Too high", "The size of the image item is too high.\n"
                                                  "Convert the image to 8 bits per pixel.")
            return

        self.active_image.create_hist_window()

        if not self.active_image.histogram_subwindows_added:
            self.central_mdi_area.addSubWindow(self.active_image.histogram_graphical)
            self.central_mdi_area.addSubWindow(self.active_image.histogram_graphical.histogram_list)
            self.active_image.histogram_subwindows_added = True

        self.active_image.histogram_graphical.show()

    @validate_active_image
    def show_intensity_profile(self, *args):
        """Create intensity profile of drawn line and show it in the sub-window."""

        self.active_image.subwindow.create_profile()

        if not self.active_image.profile_subwindow_added:
            self.central_mdi_area.addSubWindow(self.active_image.subwindow.intensity_profile)
            self.active_image.profile_subwindow_added = True

        self.active_image.subwindow.intensity_profile.show()

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
            self.active_image.calc_negation()
        else:
            self.active_image.run_operation_dialog(operation)

        self.active_image.update()

    @validate_active_image
    def image_calculator(self, *args):
        """Perform one of the double-argument point operations between two images."""

        new_image = Image.run_calculator_dialog(self.images.values())

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
            urls = event.mimeData().urls()
            files_paths = [url.toLocalFile() for url in urls]
            self.open_images(files_paths)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    app.setStyleSheet((load_style_sheet()))
    main_window.show()
    app.exec_()
