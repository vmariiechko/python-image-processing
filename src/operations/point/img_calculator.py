from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from ..operation import Operation
from .img_calculator_ui import ImageCalculatorUI


class ImageCalculator(QDialog, Operation, ImageCalculatorUI):
    """The ImageCalculator class represents a calculator between two images."""

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

        self.img_data = None
        self.img_name = None

        img_names = list(images.keys())
        self.cb_image1.addItems(img_names)
        self.cb_image2.addItems(img_names)

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Image Calculator"

        self.setWindowTitle(_window_title)
        self.label_image1.setText(_translate(_window_title, "Image 1:"))
        self.label_image2.setText(_translate(_window_title, "Image 2:"))
        self.label_operation.setText(_translate(_window_title, "Operation:"))
