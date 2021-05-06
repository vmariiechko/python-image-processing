from cv2 import filter2D, CV_64F, normalize, NORM_MINMAX
from numpy import sum, abs
from scipy.signal import convolve2d
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
        self.rbtn_two_stage_convolve.clicked.connect(self.update_form)
        self.rbtn_show_hist.clicked.connect(self.update_hist)

        self.update_form()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Convolve"

        self.setWindowTitle(_window_title)
        self.label_two_stage_convolve.setText(_translate(_window_title, "Two-stage:"))
        self.label_border_type.setText(_translate(_window_title, "Border type:"))
        self.label_kernel.setText(_translate(_window_title, "Kernel:"))

    def update_form(self):
        """Update the second kernel grid access whenever :attr:`rbtn_two_stage_convolve` clicked."""

        if self.rbtn_two_stage_convolve.isChecked():
            self.grids[1].setVisible(True)
            self.label_kernel.setText("Kernels:")
        else:
            self.grids[1].setVisible(False)
            self.label_kernel.setText("Kernel:")

        self.update_img_preview()

    def update_kernel_value(self, index, value, first_kernel):
        """
        Update kernel values whenever changed.

        :param index: The index of kernel cell, e.g. (1, 2)
        :type index: tuple[int]
        :param value: The new value of kernel cell
        :type value: int
        :param first_kernel: The flag to indicate whether the first or second kernel need to update
        :type first_kernel: bool
        """

        i, j = index

        if first_kernel:
            self.kernel1_values[i][j] = value
        else:
            self.kernel2_values[i][j] = value

        self.update_img_preview()

    def merge_kernels(self):
        """
        Merge two input kernels 3x3 to single kernel 5x5.

        :return: The new merged kernel of size 5x5
        :rtype: class:`numpy.ndarray`
        """

        return convolve2d(self.kernel1_values, self.kernel2_values, mode="full")

    def calc_convolve(self, border, kernel_values):
        """
        Convolve an image based on border type and kernel values.

        :param border: The border type for convolution, defined in BORDER_TYPES
        :type border: str
        :param kernel_values: The values of kernel matrix to convolve
        :type kernel_values: class:`numpy.ndarray`
        :return: The new convolved image data
        :rtype: class:`numpy.ndarray`
        """

        border_type = BORDER_TYPES[border]
        coeff = sum(kernel_values)

        if coeff == 0:
            coeff = 1

        kernel = kernel_values/coeff

        # Perform convolution in float 64-bit per pixel data type
        img_data = filter2D(self.img_data, CV_64F, kernel, borderType=border_type)

        # Normalize and convert image to uint8 data type
        return normalize(abs(img_data), None, 0, 255, NORM_MINMAX, dtype=0)

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate convolve based on border and kernel input values.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        border_type = self.cb_border_type.currentText()

        if self.rbtn_two_stage_convolve.isChecked():
            kernel_values = self.merge_kernels()
        else:
            kernel_values = self.kernel1_values

        self.current_img_data = self.calc_convolve(border_type, kernel_values)
        super().update_img_preview()
