from cv2 import blur, GaussianBlur, medianBlur
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from src.constants import BORDER_TYPES
from ..operation import Operation
from .smooth_ui import SmoothUI


class Smooth(QDialog, Operation, SmoothUI):
    """The Smooth class implements a local smoothing operation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform smoothing.

        Get image data and color depth from :param:`parent`.
        Set slider values based on image data.

        :param parent: The image to smooth
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.img_data = parent.data.copy()
        self.current_img_data = None

        self.cb_smooth_type.activated[str].connect(self.update_form)
        self.cb_border_type.activated[str].connect(self.update_img_preview)
        self.sb_kernel_size.valueChanged.connect(self.update_img_preview)
        self.rbtn_show_hist.clicked.connect(self.update_hist)

        self.update_form()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Smooth"

        self.setWindowTitle(_window_title)
        self.label_smooth_type.setText(_translate(_window_title, "Smooth type:"))
        self.label_kernel_size.setText(_translate(_window_title, "Kernel size:"))
        self.label_border_type.setText(_translate(_window_title, "Border type:"))

    def update_form(self):
        """Update the border type access, which isn't available for Median Blur."""

        if self.cb_smooth_type.currentText() == "Median Blur":
            self.cb_border_type.setEnabled(False)

            # image with color depth higher than 8-bit can't have kernel size higher than 4
            if self.img_data.dtype.itemsize > 1:
                self.sb_kernel_size.setValue(3)
                self.sb_kernel_size.setEnabled(False)
        else:
            self.cb_border_type.setEnabled(True)
            self.sb_kernel_size.setEnabled(True)

        self.update_img_preview()

    def calc_smooth(self, smooth, border, ksize):
        """
        Calculate the smoothing of the selected type.

        :param smooth: The smooth type to calculate, can be "Blur", "Gaussian Blur" or "Median Blur"
        :type smooth: str
        :param border: The border type for smoothing, defined in BORDER_TYPES
        :type border: str
        :param ksize: The number for NxN kernel
        :type ksize: int
        :return: The smoothed image data
        :rtype: class:`numpy.ndarray`
        """

        border_type = BORDER_TYPES[border]

        if ksize % 2 == 0:
            ksize -= 1
            self.sb_kernel_size.setValue(ksize)

        if smooth == "Blur":
            img_data = blur(self.img_data, (ksize, ksize), borderType=border_type)
        elif smooth == "Gaussian Blur":
            img_data = GaussianBlur(self.img_data, (ksize, ksize), 0, borderType=border_type)
        else:
            img_data = medianBlur(self.img_data, ksize)

        return img_data

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image smoothing based on kernel size, smooth and border type.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        smooth_type = self.cb_smooth_type.currentText()
        border_type = self.cb_border_type.currentText()
        kernel_size = self.sb_kernel_size.value()

        self.current_img_data = self.calc_smooth(smooth_type, border_type, kernel_size)
        super().update_img_preview()
