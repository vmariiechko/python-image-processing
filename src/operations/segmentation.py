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

        self.threshold_slider.setMaximum(self.color_depth - 1)
        self.threshold_slider.setProperty("value", self.color_depth // 2 - 1)

        self.cb_segmentation_type.activated[str].connect(self.update_form)
        self.rbtn_show_hist.clicked.connect(self.update_hist)
        self.threshold_slider.valueChanged.connect(self.update_thresh_value)
        self.threshold_slider.sliderReleased.connect(self.update_img_preview)

        self.update_thresh_value()
        self.update_form()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Segmentation"

        self.setWindowTitle(_window_title)
        self.label_segmentation_type.setText(_translate(_window_title, "Segmentation type:"))
        self.label_thresh_txt.setText(_translate(_window_title, "Threshold value:"))

    def update_form(self):
        """"""

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
        :return: The new updated image data
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
        :return: The new updated image data
        :rtype: class:`numpy.ndarray`
        """

        img_data = self.img_data.copy()

        for w in range(img_data.shape[0]):
            for h in range(img_data.shape[1]):
                if img_data[w][h] < thresh_value:
                    img_data[w][h] = 0

        return img_data

    def update_thresh_value(self):
        """Update :attr:`label_thresh_value` whenever is changed."""

        self.label_thresh_value.setText(str(self.threshold_slider.value()))

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image thresholding based on slider value.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        segmentation_type = self.cb_segmentation_type.currentText()
        thresh_value = self.threshold_slider.value()

        if segmentation_type == "Threshold Binary":
            img_data = self.calc_threshold_binary(thresh_value)
        elif segmentation_type == "Threshold Zero":
            img_data = self.calc_threshold_zero(thresh_value)

        self.current_img_data = img_data
        super().update_img_preview()
