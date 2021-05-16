from cv2 import filter2D, normalize, NORM_MINMAX
from numpy import array, abs
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from src.constants import BORDER_TYPES
from ..operation import Operation
from .sharpen_ui import SharpenUI


class Sharpen(QDialog, Operation, SharpenUI):
    """The Sharpen class implements a local sharpen operation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform sharpening.

        Get image data from :param:`parent`.
        Convert to uint8 data type.

        :param parent: The image to sharpen
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.img_data = parent.data.copy()
        self.current_img_data = None

        if self.img_data.dtype.itemsize > 1:
            self.img_data = normalize(abs(self.img_data), None, 0, 255, NORM_MINMAX, dtype=0)

        self.cb_border_type.activated[str].connect(self.update_img_preview)
        self.rbtn_mask1.clicked.connect(self.update_img_preview)
        self.rbtn_mask2.clicked.connect(self.update_img_preview)
        self.rbtn_mask3.clicked.connect(self.update_img_preview)
        self.rbtn_show_hist.clicked.connect(self.update_hist)

        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Sharpen"

        self.setWindowTitle(_window_title)
        self.label_border_type.setText(_translate(_window_title, "Border type:"))
        self.label_masks.setText(_translate(_window_title, "Laplacian masks:"))

    def calc_sharpen(self, border):
        """
        Sharpen an image based on chosen Laplacian mask.

        :param border: The border type for sharpening, defined in BORDER_TYPES
        :type border: str
        :return: The image sharpening
        :rtype: class:`numpy.ndarray`
        """

        border_type = BORDER_TYPES[border]

        if self.rbtn_mask1.isChecked():
            mask = array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        elif self.rbtn_mask2.isChecked():
            mask = array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        else:
            mask = array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]])

        return filter2D(self.img_data, -1, mask, borderType=border_type)

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image sharpen.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        border = self.cb_border_type.currentText()

        self.current_img_data = self.calc_sharpen(border)
        super().update_img_preview()
