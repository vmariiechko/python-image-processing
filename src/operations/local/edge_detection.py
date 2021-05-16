from cv2 import (Sobel, Laplacian, Canny, CV_64F, normalize,
                 NORM_MINMAX, add, filter2D)
from numpy import array, abs
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from src.constants import BORDER_TYPES
from ..operation import Operation
from .edge_detection_ui import EdgeDetectionUI, DirectionalEdgeDetectionUI


class EdgeDetection(QDialog, Operation, EdgeDetectionUI):
    """The EdgeDetection class implements a local edge detection operation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform edge detection.

        Get image data and color depth from :param:`parent`.
        Convert to uint8 data type.
        Set spin box maximum values.

        :param parent: The image to detect edges
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.color_depth = parent.color_depth
        self.img_data = parent.data.copy()
        self.current_img_data = None

        # Convertion, Canny method operates only on uint8 data type
        if self.img_data.dtype.itemsize > 1:
            self.img_data = normalize(abs(self.img_data), None, 0, 255, NORM_MINMAX, dtype=0)
            self.color_depth = 256

        self.sb_low_threshold.setMaximum(self.color_depth - 2)
        self.sb_high_threshold.setMaximum(self.color_depth - 1)
        self.sb_low_threshold.setValue(self.color_depth // 2.55)
        self.sb_high_threshold.setValue(self.color_depth // 1.275)

        self.cb_edge_dt_type.activated[str].connect(self.update_form)
        self.cb_border_type.activated[str].connect(self.update_img_preview)

        self.sb_kernel_size.valueChanged.connect(self.update_img_preview)
        self.sb_low_threshold.valueChanged.connect(self.validate_low_value)
        self.sb_high_threshold.valueChanged.connect(self.validate_high_value)

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

        self.update_img_preview()

    def validate_high_value(self):
        """Filter threshold range to be valid for the upper value."""

        high_threshold = self.sb_high_threshold.value()

        if high_threshold <= self.sb_low_threshold.value():
            self.sb_low_threshold.setValue(high_threshold - 1)

        self.update_img_preview()

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

        self.update_img_preview()

    def calc_edges(self, edge_type, border, ksize, threshold):
        """
        Detect image edges for selected edge type.

        To get better results, Sobel and Laplacian methods
        perform edge detection in int16 data type.

        :param edge_type: The type of edge detecting, can be "Sobel", "Laplacian", "Canny"
        :type edge_type: str
        :param border: The border type for edge detection, defined in BORDER_TYPES
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

        - Calculate image edges based on form parameters.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        edge = self.cb_edge_dt_type.currentText()
        border = self.cb_border_type.currentText()
        ksize = self.sb_kernel_size.value()
        low_thresh = self.sb_low_threshold.value()
        high_thresh = self.sb_high_threshold.value()

        self.current_img_data = self.calc_edges(edge, border, ksize, (low_thresh, high_thresh))
        super().update_img_preview()


class DirectionalEdgeDetection(QDialog, Operation, DirectionalEdgeDetectionUI):
    """The DirectionalEdgeDetection class implements a local direction edge detection operation."""

    # Map directions to Prewitt masks
    DIRECTION_MASKS = {
        "E": array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),
        "SE": array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]]),
        "S": array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]),
        "SW": array([[0, -1, -1], [1, 0, -1], [1, 1, 0]]),
        "W": array([[1, 0, -1], [1, 0, -1], [1, 0, -1]]),
        "NW": array([[1, 1, 0], [1, 0, -1], [0, -1, -1]]),
        "N": array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]]),
        "NE": array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]]),
    }

    def __init__(self, parent):
        """
        Create a new dialog window to perform direction edge detection.

        Get image data from :param:`parent`.
        Convert to uint8 data type.

        :param parent: The image to detect edges
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
        self.cb_edge_dt_direction.activated[str].connect(self.update_img_preview)

        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Directional Edge Detection"

        self.setWindowTitle(_window_title)
        self.label_edge_dt_direction.setText(_translate(_window_title, "Direction:"))
        self.label_border_type.setText(_translate(_window_title, "Border type:"))
        self.label_masks_txt.setText(_translate(_window_title, "Prewitt direction masks:\n"))

    def calc_edges(self, direction, border):
        """
        Detect image edges for selected direction.
        Direction specifies Prewitt mask.

        :param direction: The Prewitt mask direction, defined in DIRECTION_MASKS
        :param border: The border type for edge detection, defined in BORDER_TYPES
        :type border: str
        :return: The new image data with detected edges
        :rtype: class:`numpy.ndarray`
        """

        border_type = BORDER_TYPES[border]
        direction_mask = self.DIRECTION_MASKS[direction]

        return filter2D(self.img_data, -1, direction_mask, borderType=border_type)

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image edges based on chosen direction and border.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        direction = self.cb_edge_dt_direction.currentText()
        border = self.cb_border_type.currentText()

        self.current_img_data = self.calc_edges(direction, border)
        super().update_img_preview()
