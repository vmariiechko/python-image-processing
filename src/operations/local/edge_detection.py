from cv2 import Sobel, Laplacian, Canny, CV_64F, normalize, NORM_MINMAX, add
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from numpy import abs

from src.constants import BYTES_PER_PIXEL_2_BW_FORMAT, BORDER_TYPES
from .edge_detection_ui import EdgeDetectionUI


class EdgeDetection(QDialog, EdgeDetectionUI):
    """The EdgeDetection class implements a local edge detection operation."""

    def __init__(self, parent):
        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.color_depth = parent.color_depth
        self.img_data = parent.img_data.copy()
        self.current_img_data = None

        # Convert to uint8 data type, Canny method operates only on CV_8U
        if self.color_depth > 256:
            self.img_data = normalize(abs(self.img_data), None, 0, 255, NORM_MINMAX, dtype=0)
            self.color_depth = 256

        self.sb_low_threshold.setMaximum(self.color_depth - 2)
        self.sb_high_threshold.setMaximum(self.color_depth - 1)
        self.sb_low_threshold.setValue(self.color_depth // 2.55)
        self.sb_high_threshold.setValue(self.color_depth // 1.275)

        self.cb_edge_dt_type.activated[str].connect(self.update_img_preview)
        self.cb_edge_dt_type.activated[str].connect(self.update_form)
        self.cb_border_type.activated[str].connect(self.update_img_preview)

        self.sb_kernel_size.valueChanged.connect(self.update_img_preview)
        self.sb_low_threshold.valueChanged.connect(self.update_img_preview)
        self.sb_low_threshold.valueChanged.connect(self.validate_low_value)
        self.sb_high_threshold.valueChanged.connect(self.update_img_preview)
        self.sb_high_threshold.valueChanged.connect(self.validate_high_value)

        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(self.accept_changes)

        self.update_img_preview()
        self.update_form()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Edge Detection"

        self.setWindowTitle(_window_title)
        self.label_edge_dt_type.setText(_translate(_window_title, "Detection type:"))
        self.label_kernel_size.setText(_translate(_window_title, "Kernel size:"))
        self.label_border_type.setText(_translate(_window_title, "Border type:"))
        self.label_low_threshold.setText(_translate(_window_title, "Threshold Min:"))
        self.label_high_threshold.setText(_translate(_window_title, "Threshold Max:"))

    def validate_low_value(self):
        """Filter threshold range to be valid for the lower value."""

        low_threshold = self.sb_low_threshold.value()
        if low_threshold >= self.sb_high_threshold.value():
            self.sb_high_threshold.setValue(low_threshold + 1)

    def validate_high_value(self):
        """Filter threshold range to be valid for the upper value."""

        high_threshold = self.sb_high_threshold.value()
        if high_threshold <= self.sb_low_threshold.value():
            self.sb_low_threshold.setValue(high_threshold - 1)

    def update_form(self):
        """
        Update lower:upper threshold spin box, border, and kernel size access.

        The threshold range is available only for Canny detection.
        Border type and kernel size are available for other methods.
        """

        if self.cb_edge_dt_type.currentText() == "Canny":
            self.sb_low_threshold.setEnabled(True)
            self.sb_high_threshold.setEnabled(True)
            self.sb_kernel_size.setEnabled(False)
            self.cb_border_type.setEnabled(False)
        else:
            self.sb_low_threshold.setEnabled(False)
            self.sb_high_threshold.setEnabled(False)
            self.sb_kernel_size.setEnabled(True)
            self.cb_border_type.setEnabled(True)

    def calc_edges(self, edge_type, border, ksize, threshold):
        """
        Detect image edges for selected edge type.

        To get better results, Sobel and Laplacian methods
        perform edge detection in int16 data type

        :param edge_type: The type of edge detecting, can be "Sobel", "Laplacian", "Canny"
        :type edge_type: str
        :param border: The border type for smoothing, defined in BORDER_TYPES
        :type border: str
        :param ksize: The number for NxN kernel
        :type ksize: int
        :param threshold: The lower:upper threshold values for Canny detection
        :type threshold: tuple[int]
        :return: The new image data with detected edges
        :rtype: class:`numpy.ndarray`
        """

        border_type = BORDER_TYPES[border]

        # The kernel size must be odd and not larger than 31
        if ksize % 2 == 0:
            ksize -= 1
            self.sb_kernel_size.setValue(ksize)

        # Calculate Sobel detection for OX and OY axis and sum results
        if edge_type == "Sobel":
            img_data_x = Sobel(self.img_data, CV_64F, 1, 0, ksize=ksize, borderType=border_type)
            img_data_y = Sobel(self.img_data, CV_64F, 0, 1, ksize=ksize, borderType=border_type)
            img_data = add(img_data_x, img_data_y)

        elif edge_type == "Laplacian":
            img_data = Laplacian(self.img_data, CV_64F, ksize=ksize, borderType=border_type)

        else:
            img_data = Canny(self.img_data, threshold[0], threshold[1])

        # Normalize and convert image to uint8 data type
        return normalize(abs(img_data), None, 0, 255, NORM_MINMAX, dtype=0)

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image edges based on form parameters
        - Convert new image data to :class:`PyQt5.QtGui.QImage`.
        - Reload the image to the preview window.
        """

        edge = self.cb_edge_dt_type.currentText()
        border = self.cb_border_type.currentText()
        ksize = self.sb_kernel_size.value()
        low_thresh = self.sb_low_threshold.value()
        high_thresh = self.sb_high_threshold.value()

        img_data = self.calc_edges(edge, border, ksize, (low_thresh, high_thresh))
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
