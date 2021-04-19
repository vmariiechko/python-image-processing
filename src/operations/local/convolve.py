from cv2 import filter2D
from numpy import sum
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from src.constants import BORDER_TYPES
from ..operation import Operation
from .convolve_ui import ConvolveUI


class Convolve(QDialog, Operation, ConvolveUI):
    """The Convolve class implements a local convolve operation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform convolution.
        Get image data from :param:`parent`.

        :param parent: The image to convolve
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.img_data = parent.img_data.copy()
        self.current_img_data = None

        self.cb_border_type.activated[str].connect(self.update_img_preview)
        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Convolve"

        self.setWindowTitle(_window_title)
        self.label_border_type.setText(_translate(_window_title, "Border type:"))
        self.label_kernel.setText(_translate(_window_title, "Kernel:"))

    def update_kernel_value(self, index, value):
        """
        Update kernel values whenever is changed.

        :param index: The index of kernel cell. Can be (1, 2)
        :type index: tuple[int]
        :param value: The new value of kernel cell
        :type value: int
        """

        i, j = index
        self.kernel_values[i][j] = value
        self.update_img_preview()

    def calc_convolve(self, border):
        """
        Convolve an image based on border type and input kernel values.

        :param border: The border type for convolution, defined in BORDER_TYPES
        :type border: str
        :return: The new convolved image data
        :rtype: class:`numpy.ndarray`
        """

        border_type = BORDER_TYPES[border]
        coeff = sum(self.kernel_values)

        if coeff == 0:
            coeff = 1

        kernel = self.kernel_values/coeff
        return filter2D(self.img_data, -1, kernel, borderType=border_type)

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate convolve based on border and kernel.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        border_type = self.cb_border_type.currentText()
        self.current_img_data = self.calc_convolve(border_type)
        super().update_img_preview()
