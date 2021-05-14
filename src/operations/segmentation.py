from cv2 import threshold, adaptiveThreshold, THRESH_BINARY, ADAPTIVE_THRESH_MEAN_C, ADAPTIVE_THRESH_GAUSSIAN_C
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from .operation import Operation
from .segmentation_ui import SegmentationUI


class Segmentation(QDialog, Operation, SegmentationUI):
    """The Segmentation class represents segmentation operations."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform segmentation.

        Get image data and color depth from :param:`parent`.
        Set slider values based on image data.

        :param parent: The image to segmentate
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.color_depth = parent.color_depth
        self.img_data = parent.img_data.copy()
        self.current_img_data = None

        self.segmentation_slider.setMaximum(self.color_depth - 1)
        self.segmentation_slider.setProperty("value", self.color_depth // 2 - 1)

        self.cb_segmentation_type.activated[str].connect(self.update_form)
        self.rbtn_show_hist.clicked.connect(self.update_hist)
        self.segmentation_slider.valueChanged.connect(self.update_slider_value)
        self.segmentation_slider.sliderReleased.connect(self.update_img_preview)

        self.update_slider_value()
        self.update_form()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Segmentation"

        self.setWindowTitle(_window_title)
        self.label_segmentation_type.setText(_translate(_window_title, "Segmentation type:"))
        self.label_slider_txt.setText(_translate(_window_title, "Threshold value:"))

    def update_form(self):
        """Update the slider minimum value and slider text based on segmentation type."""

        segmentation_type = self.cb_segmentation_type.currentText()

        if segmentation_type in ("Threshold Binary", "Threshold Zero"):
            self.label_slider_txt.setText("Threshold value:")
            self.segmentation_slider.setMinimum(0)
        elif segmentation_type in ("Adaptive Mean Threshold", "Adaptive Gaussian Threshold"):
            self.label_slider_txt.setText("Block size:")
            self.segmentation_slider.setMinimum(3)

        self.update_img_preview()

    def calc_threshold_binary(self, thresh_value):
        """
        Calculate threshold binary point operation.

        if the pixel is higher than :param:`thresh_value`,
        then the new pixel intensity is set to a maximum
        value - :attr:`color_depth`-1.
        Otherwise, the pixels are set to 0

        :param thresh_value: The value for segmentation
        :type thresh_value: int
        :return: The new thresholded image data
        :rtype: class:`numpy.ndarray`
        """

        img_data = self.img_data.copy()

        for w in range(img_data.shape[0]):
            for h in range(img_data.shape[1]):
                img_data[w][h] = self.color_depth - 1 if img_data[w][h] > thresh_value else 0

        return img_data

    def calc_threshold_zero(self, thresh_value):
        """
        Calculate threshold to zero point operation.

        If the pixel is lower than :param:`thresh_value`,
        the new pixel value will be set to 0.

        :param thresh_value: The value for segmentation
        :type thresh_value: int
        :return: The new thresholded image data
        :rtype: class:`numpy.ndarray`
        """

        img_data = self.img_data.copy()

        for w in range(img_data.shape[0]):
            for h in range(img_data.shape[1]):
                if img_data[w][h] < thresh_value:
                    img_data[w][h] = 0

        return img_data

    def calc_adaptive_thresh(self, method, block_size):
        """
        Calculate adaptive threshold based on method and block size.

        :param method: The method to perform, can be: "Mean" or "Gaussian"
        :type method: str
        :param block_size: The value for block size
        :type block_size: int
        :return: The new thresholded image data
        :rtype: class:`numpy.ndarray`
        """

        # Validate block size value to be odd
        if block_size % 2 == 0:
            block_size -= 1
            self.segmentation_slider.setProperty("value", block_size)

        adaptive_method = ADAPTIVE_THRESH_MEAN_C if method == "Mean" else ADAPTIVE_THRESH_GAUSSIAN_C

        return adaptiveThreshold(self.img_data, 255, adaptive_method, THRESH_BINARY, block_size, 5)

    def update_slider_value(self):
        """Update :attr:`label_slider_value` whenever is changed."""

        self.label_slider_value.setText(str(self.segmentation_slider.value()))

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image segmentation based on type and slider value.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        segmentation_type = self.cb_segmentation_type.currentText()
        slider_value = self.segmentation_slider.value()

        if segmentation_type == "Threshold Binary":
            img_data = self.calc_threshold_binary(slider_value)
        elif segmentation_type == "Threshold Zero":
            img_data = self.calc_threshold_zero(slider_value)
        elif segmentation_type == "Adaptive Mean Threshold":
            img_data = self.calc_adaptive_thresh("Mean", slider_value)
        elif segmentation_type == "Adaptive Gaussian Threshold":
            img_data = self.calc_adaptive_thresh("Gaussian", slider_value)

        self.current_img_data = img_data
        super().update_img_preview()
