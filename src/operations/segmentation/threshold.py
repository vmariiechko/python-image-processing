from cv2 import (threshold, adaptiveThreshold, THRESH_BINARY, THRESH_OTSU,
                 ADAPTIVE_THRESH_MEAN_C, ADAPTIVE_THRESH_GAUSSIAN_C,
                 normalize, NORM_MINMAX)
from numpy import abs
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from ..operation import Operation
from .threshold_ui import ThresholdUI


class Threshold(QDialog, Operation, ThresholdUI):
    """The Threshold class implements a thresholding point operation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform thresholding.

        Get image data and color depth from :param:`parent`.
        Set slider values based on image data.

        :param parent: The image to threshold
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.color_depth = parent.color_depth
        self.img_data = parent.data.copy()
        self.current_img_data = None

        self.threshold_slider.setMaximum(self.color_depth - 1)
        self.threshold_slider.setProperty("value", self.color_depth // 2 - 1)

        self.cb_threshold_type.activated[str].connect(self.update_form)
        self.rbtn_show_hist.clicked.connect(self.update_hist)
        self.threshold_slider.valueChanged.connect(self.update_slider_value)
        self.threshold_slider.sliderReleased.connect(self.update_img_preview)

        self.update_slider_value()
        self.update_form()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Threshold"

        self.setWindowTitle(_window_title)
        self.label_threshold_type.setText(_translate(_window_title, "Threshold type:"))
        self.label_slider_txt.setText(_translate(_window_title, "Threshold value:"))

    def update_form(self):
        """Update the slider behavior and slider text based on threshold type."""

        threshold_type = self.cb_threshold_type.currentText()

        if threshold_type in ("Threshold Binary", "Threshold Zero"):
            self.label_slider_txt.setText("Threshold value:")
            self.threshold_slider.setEnabled(True)
            self.threshold_slider.setMinimum(0)
            self.threshold_slider.setMaximum(self.color_depth - 1)
            self.threshold_slider.setProperty("value", self.color_depth // 2 - 1)
        elif threshold_type in ("Adaptive Mean Threshold", "Adaptive Gaussian Threshold"):
            self.label_slider_txt.setText("Block size:")
            self.threshold_slider.setEnabled(True)
            self.threshold_slider.setMinimum(3)
            self.threshold_slider.setMaximum(255)
            self.threshold_slider.setProperty("value", 127)
        else:
            self.label_slider_txt.setText("Threshold value:")
            self.threshold_slider.setEnabled(False)
            self.threshold_slider.setMaximum(self.color_depth - 1)

        self.update_img_preview()

    def calc_threshold_binary(self, thresh_value):
        """
        Calculate threshold binary point operation.

        if the pixel is higher than :param:`thresh_value`,
        then the new pixel intensity is set to a maximum
        value - :attr:`color_depth`-1.
        Otherwise, the pixels are set to 0

        :param thresh_value: The value for thresholding
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

        :param thresh_value: The value for thresholding
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
            self.threshold_slider.setProperty("value", block_size)

        # Conversion, adaptive threshold operates only on uint8 data type
        if self.img_data.dtype.itemsize > 1:
            img_data = normalize(abs(self.img_data), None, 0, 255, NORM_MINMAX, dtype=0)
        else:
            img_data = self.img_data

        adaptive_method = ADAPTIVE_THRESH_MEAN_C if method == "Mean" else ADAPTIVE_THRESH_GAUSSIAN_C

        return adaptiveThreshold(img_data, 255, adaptive_method, THRESH_BINARY, block_size, 5)

    def calc_theshold_otsu(self):
        """Calculate Otsu's thresholding."""

        thresh_value, img_data = threshold(self.img_data, 0, self.color_depth-1, THRESH_BINARY + THRESH_OTSU)

        self.label_slider_value.setText(str(int(thresh_value)))
        self.threshold_slider.setProperty("value", thresh_value)

        return img_data

    def update_slider_value(self):
        """Update :attr:`label_slider_value` whenever is changed."""

        self.label_slider_value.setText(str(self.threshold_slider.value()))

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image thresholding based on type and slider value.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        threshold_type = self.cb_threshold_type.currentText()
        slider_value = self.threshold_slider.value()

        if threshold_type == "Threshold Binary":
            img_data = self.calc_threshold_binary(slider_value)
        elif threshold_type == "Threshold Zero":
            img_data = self.calc_threshold_zero(slider_value)
        elif threshold_type == "Adaptive Mean Threshold":
            img_data = self.calc_adaptive_thresh("Mean", slider_value)
        elif threshold_type == "Adaptive Gaussian Threshold":
            img_data = self.calc_adaptive_thresh("Gaussian", slider_value)
        else:
            img_data = self.calc_theshold_otsu()

        self.current_img_data = img_data
        super().update_img_preview()
