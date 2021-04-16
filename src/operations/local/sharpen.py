from cv2 import filter2D, normalize, NORM_MINMAX, CV_8U
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from numpy import array, abs

from src.constants import BYTES_PER_PIXEL_2_BW_FORMAT, BORDER_TYPES
from .sharpen_ui import SharpenUI


class Sharpen(QDialog, SharpenUI):
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

        self.img_data = parent.img_data.copy()
        self.current_img_data = None

        if self.img_data.dtype.itemsize > 1:
            self.img_data = normalize(abs(self.img_data), None, 0, 255, NORM_MINMAX, dtype=0)

        self.cb_border_type.activated[str].connect(self.update_img_preview)
        self.rbtn_mask1.clicked.connect(self.update_img_preview)
        self.rbtn_mask2.clicked.connect(self.update_img_preview)
        self.rbtn_mask3.clicked.connect(self.update_img_preview)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(self.accept_changes)

        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Sharpen"

        self.setWindowTitle(_window_title)
        self.label_border_type.setText(_translate(_window_title, "Border type:"))
        self.label_masks.setText(_translate(_window_title, "Laplacian mask:"))

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

        return filter2D(self.img_data, CV_8U, mask, borderType=border_type)

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image sharpen
        - Convert new image data to :class:`PyQt5.QtGui.QImage`.
        - Reload the image to the preview window.
        """

        border = self.cb_border_type.currentText()

        img_data = self.calc_sharpen(border)
        height, width = img_data.shape[:2]

        if len(img_data.shape) == 2:
            pixel_bytes = img_data.dtype.itemsize
            image = QImage(img_data, width, height, BYTES_PER_PIXEL_2_BW_FORMAT[pixel_bytes])
        else:
            image = QImage(img_data, width, height, 3 * width, QImage.Format_BGR888)

        pixmap = QPixmap(image)
        self.label_image.setPixmap(pixmap)
        self.current_img_data = img_data

    def accept_changes(self):
        """Accept changed image data to the original one."""

        self.img_data = self.current_img_data
        self.accept()
