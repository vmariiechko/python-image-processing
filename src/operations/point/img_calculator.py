from cv2 import add, subtract, addWeighted, resize, bitwise_and, bitwise_or, bitwise_xor
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap

from src.constants import BYTES_PER_PIXEL_2_BW_FORMAT
from .img_calculator_ui import ImageCalculatorUI


class ImageCalculator(QDialog, ImageCalculatorUI):
    """The ImageCalculator class represents a calculator between two images."""

    OPERATIONS = {
        "Add": add,
        "Subtract": subtract,
        "AND": bitwise_and,
        "OR": bitwise_or,
        "XOR": bitwise_xor,
    }

    def __init__(self, images):
        """
        Create a new dialog window to perform image calculation.

        Fill out combo boxes with image names from :param:`images`

        :param images: The images to perform calculation, dict[img_name:data]
        :type images: dict
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.images = images
        self.img_data = None
        self.img_name = None
        self.match = False
        self.current_img_data = None

        img_names = list(images.keys())
        self.cb_image1.addItems(img_names)
        self.cb_image2.addItems(img_names)

        self.cb_image1.activated[str].connect(self.update_gamma_range)
        self.cb_image2.activated[str].connect(self.update_calculation)
        self.cb_operation.activated[str].connect(self.update_form)

        self.sb_weight1.valueChanged.connect(self.update_calculation)
        self.sb_weight2.valueChanged.connect(self.update_calculation)
        self.sb_gamma.valueChanged.connect(self.update_calculation)

        self.rbtn_resize1.clicked.connect(self.update_rbtns)
        self.rbtn_resize2.clicked.connect(self.update_rbtns)

        self.update_form()
        self.update_gamma_range()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Image Calculator"

        self.setWindowTitle(_window_title)
        self.label_image1.setText(_translate(_window_title, "Image 1:"))
        self.label_image2.setText(_translate(_window_title, "Image 2:"))
        self.label_weight1.setText(_translate(_window_title, "<div>Weight &alpha;:</div>"))
        self.label_weight2.setText(_translate(_window_title, "<div>Weight &beta;:</div>"))
        self.label_operation.setText(_translate(_window_title, "Operation:"))
        self.label_gamma.setText(_translate(_window_title, "<div>Gamma &gamma;:</div>"))

    def update_gamma_range(self):
        """Validate the gamma spin box to be in the color depth range of the first image."""

        img_data = self.images[self.cb_image1.currentText()]
        img_depth = 2 ** (8 * img_data.dtype.itemsize)

        self.sb_gamma.setMinimum(-img_depth + 1)
        self.sb_gamma.setMaximum(img_depth - 1)

        self.update_calculation()

    def update_form(self):
        """
        Update the image weights and gamma form access,
        which is available only for Blend operation.
        """

        if self.cb_operation.currentText() == "Blend":
            self.sb_weight1.setEnabled(True)
            self.sb_weight2.setEnabled(True)
            self.sb_gamma.setEnabled(True)
        else:
            self.sb_weight1.setEnabled(False)
            self.sb_weight2.setEnabled(False)
            self.sb_gamma.setEnabled(False)

        self.update_calculation()

    def update_rbtns(self):
        """Validate only one radio button to be checked."""

        if self.rbtn_resize1 == self.sender():
            self.rbtn_resize2.setChecked(False)
        else:
            self.rbtn_resize1.setChecked(False)

        self.update_calculation()

    @staticmethod
    def validate_images(img1_data, img2_data):
        """
        Validate images whether they match to perform the calculation.

        The images must have the same:

        - Dimensions.
        - Number of channels.
        - Color depth.

        `True` if the images match to calculation,
        `False` otherwise.

        :param img1_data: The first image data to validate
        :type img1_data: class:`numpy.ndarray`
        :param img2_data: The second image data to validate
        :type img2_data: class:`numpy.ndarray`
        :return: The status of validation. (match, fail message) - (bool, str)
        :rtype: tuple
        """

        # Validate dimensions
        if img1_data.shape[:2] != img2_data.shape[:2]:
            return False, "The image sizes differs"

        # Validate the number of channels
        if len(img1_data.shape) == 3 and len(img2_data.shape) == 3:
            if img1_data.shape[2] != img2_data.shape[2]:
                return False, "The number of channels differs"
        else:
            if len(img1_data.shape) != 2 or len(img2_data.shape) != 2:
                return False, "The number of channels differs"

        # Validate color depth
        if img1_data.dtype.itemsize != img2_data.dtype.itemsize:
            return False, "The image color depths differs"

        # Validation passed successfully
        return True, None

    def calculate(self, img1_data, img2_data, operation_name):
        """
        Perform specified operation between two images.

        Available operations are in :attr:`OPERATIONS`.

        :param img1_data: The first image data to perform calculation
        :type img1_data: class:`numpy.ndarray`
        :param img2_data: The second image data to perform calculation
        :type img2_data: class:`numpy.ndarray`
        :param operation_name: The operation name to perform between images
        :type operation_name: str
        :return: The new calculated image data
        :rtype: class:`numpy.ndarray`
        """

        if operation_name == "Blend":
            weight1 = self.sb_weight1.value()
            weight2 = self.sb_weight2.value()
            gamma = self.sb_gamma.value()
            img_data = addWeighted(img1_data, weight1, img2_data, weight2, gamma)
        else:
            operation = self.OPERATIONS[operation_name]
            img_data = operation(img1_data, img2_data)

        return img_data

    def update_calculation(self):
        """
        Update calculation whenever changed form.

        - Get the image data based on chosen images.
        - Resize the image if the radio button is checked.
        - Validate images.
        - Perform calculations based on chosen operations and images.
        """

        img1_name = self.cb_image1.currentText()
        img2_name = self.cb_image2.currentText()
        operation_name = self.cb_operation.currentText()

        self.img_name = "Result of " + img1_name
        img1_data = self.images[img1_name]
        img2_data = self.images[img2_name]

        if self.rbtn_resize1.isChecked():
            img1_data = resize(img1_data, img2_data.shape[:2])
        elif self.rbtn_resize2.isChecked():
            img2_data = resize(img2_data, img1_data.shape[:2])

        self.match, fail_msg = self.validate_images(img1_data, img2_data)
        if not self.match:
            self.label_image.setText(fail_msg)
            self.adjustSize()
            return

        self.img_data = self.calculate(img1_data, img2_data, operation_name)
        self.update_img_preview(self.img_data)

    def update_img_preview(self, img_data):
        """
        Update image preview window.

        - Reload image preview using the base :class:`operation.Operation` method.
        """

        height, width = img_data.shape[:2]

        if len(img_data.shape) == 2:
            pixel_bytes = img_data.dtype.itemsize
            image = QImage(img_data, width, height, BYTES_PER_PIXEL_2_BW_FORMAT[pixel_bytes])
        else:
            image = QImage(img_data, width, height, 3 * width, QImage.Format_BGR888)

        pixmap = QPixmap(image)
        self.label_image.setPixmap(pixmap)
        self.adjustSize()

    def accept_changes(self):
        """Accept changed image data to the original one."""

        if self.match:
            self.accept()
