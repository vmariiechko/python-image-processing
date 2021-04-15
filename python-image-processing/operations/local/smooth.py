from cv2 import blur, GaussianBlur
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap

from .smooth_ui import SmoothUI


class Smooth(QDialog, SmoothUI):
    """The Smooth class implements a local smoothing operation."""

    BORDER_TYPES = {
        "Isolated": 16,
        "Reflect": 2,
        "Replicate": 1,
    }

    bytes_per_pixel = {
        1: QImage.Format_Grayscale8,
        2: QImage.Format_Grayscale16,
    }

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

        self.img_data = parent.image.copy()
        self.current_img_data = None

        self.cb_smooth_type.activated[str].connect(self.update_img_preview)
        self.cb_border_type.activated[str].connect(self.update_img_preview)

        self.sb_kernel_size.valueChanged.connect(self.update_img_preview)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(self.accept_changes)

        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Smooth"

        self.setWindowTitle(_window_title)
        self.label_smooth_type.setText(_translate(_window_title, "Smooth type:"))
        self.label_kernel_size.setText(_translate(_window_title, "Kernel size:"))
        self.label_border_type.setText(_translate(_window_title, "Border type:"))

    def calc_smooth(self, smooth, border, ksize):
        """
        Calculate the smoothing of the selected type.

        :param smooth: The smooth type to calculate, can be "Blur" or "Gaussian Blur"
        :type smooth: str
        :param border: The border type for smoothing, defined in BORDER_TYPES
        :type border: str
        :param ksize: The number for NxN kernel
        :type ksize: int
        :return: The smoothed image data
        :rtype: class:`numpy.ndarray`
        """

        border_type = self.BORDER_TYPES[border]

        if smooth == "Blur":
            img_data = blur(self.img_data, (ksize, ksize), borderType=border_type)
        else:
            if ksize % 2 == 0:
                ksize -= 1
                self.sb_kernel_size.setValue(ksize)

            img_data = GaussianBlur(self.img_data, (ksize, ksize), 0, borderType=border_type)

        return img_data

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image smoothing based on kernel size, smooth and border type
        - Convert new image data to :class:`PyQt5.QtGui.QImage`.
        - Reload the image to the preview window.
        """

        smooth_type = self.cb_smooth_type.currentText()
        border_type = self.cb_border_type.currentText()
        kernel_size = self.sb_kernel_size.value()

        img_data = self.calc_smooth(smooth_type, border_type, kernel_size)
        height, width = img_data.shape[:2]

        if len(img_data.shape) == 2:
            color_depth = img_data.dtype.itemsize
            image = QImage(img_data, width, height, self.bytes_per_pixel[color_depth])
        else:
            image = QImage(img_data, width, height, 3*width, QImage.Format_BGR888)

        pixmap = QPixmap(image)
        self.label_image.setPixmap(pixmap)
        self.current_img_data = img_data

    def accept_changes(self):
        """Accept changed image data to the original one."""

        self.img_data = self.current_img_data
        self.accept()
