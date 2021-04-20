from cv2 import add, subtract
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from ..operation import Operation
from .img_calculator_ui import ImageCalculatorUI


class ImageCalculator(QDialog, Operation, ImageCalculatorUI):
    """The ImageCalculator class represents a calculator between two images."""

    OPERATIONS = {
        "Add": add,
        "Substract": subtract
    }

    def __init__(self, images):
        """
        Create a new dialog window to perform image calculation.

        Fill out spin boxes with image names from :param:`images`

        :param images: The images to perform calculation, dict[img_name:img_data]
        :type images: dict
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.images = images
        self.img_data = None
        self.img_name = None
        self.current_img_data = None

        img_names = list(images.keys())
        self.cb_image1.addItems(img_names)
        self.cb_image2.addItems(img_names)

        self.cb_image1.activated[str].connect(self.update_img_preview)
        self.cb_image2.activated[str].connect(self.update_img_preview)
        self.cb_operation.activated[str].connect(self.update_img_preview)

        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Image Calculator"

        self.setWindowTitle(_window_title)
        self.label_image1.setText(_translate(_window_title, "Image 1:"))
        self.label_image2.setText(_translate(_window_title, "Image 2:"))
        self.label_operation.setText(_translate(_window_title, "Operation:"))

    def calculate(self, img1_name, img2_name, operation_name):
        """
        Perform specified calculation between two images.

        Available operations are in :attr:`OPERATIONS`.

        :param img1_name: The first image name to perform calculation
        :type img1_name: str
        :param img2_name: The second image name to perform calculation
        :type img2_name: str
        :param operation_name: The operation name to perform between images
        :type operation_name: str
        :return: The new calculated image data
        :rtype: class:`numpy.ndarray`
        """

        img1_data = self.images[img1_name]
        img2_data = self.images[img2_name]
        operation = self.OPERATIONS[operation_name]

        return operation(img1_data, img2_data)

    def update_img_preview(self):
        """
        Update image preview window.

        - Perform calculations based on chosen operations and images.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        img1_name = self.cb_image1.currentText()
        img2_name = self.cb_image2.currentText()
        operation_name = self.cb_operation.currentText()

        self.current_img_data = self.calculate(img1_name, img2_name, operation_name)
        self.img_name = "Result of " + img1_name
        super(ImageCalculator, self).update_img_preview()
