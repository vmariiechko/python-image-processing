from PyQt5.QtWidgets import QDialog

from ..operation import Operation
from .posterize_ui import PosterizeUI


class Posterize(QDialog, Operation, PosterizeUI):
    """The Posterize class implements a posterizing point operation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform posterizing.

        Get image data and color depth from :param:`parent`.
        Set slider values based on image data.

        :param parent: The image to posterize
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.setWindowTitle("Posterize")

        self.color_depth = parent.color_depth
        self.img_data = parent.img_data.copy()
        self.current_img_data = None

        self.bins_slider.setMinimum(2)
        self.bins_slider.setMaximum(self.color_depth // 2 - 1)
        self.bins_slider.setProperty("value", self.color_depth // 16)

        self.bins_slider.valueChanged.connect(self.update_bins_value)
        self.bins_slider.sliderReleased.connect(self.update_img_preview)

        self.update_bins_value()
        self.update_img_preview()

    def __apply_lut(self, lut):
        """
        Apply LUT to the image.

        :param lut: The Lookup Table
        :type lut: list[int]
        """

        img_data = self.img_data.copy()

        for w in range(img_data.shape[0]):
            for h in range(img_data.shape[1]):
                img_data[w][h] = lut[img_data[w][h]]

        return img_data

    def calc_posterize_lut(self, bins_num):
        """
        Calculate LUT for posterizing point operation.

        Based on given :param:`bins_num`:

        - Calculate length for a single bin.
        - Calculate ranges for bins.
        - Create LUT for ranges.

        :param bins_num: The number of bins to posterize
        :type bins_num: int
        :return: The Lookup Table
        :rtype: list[int]
        """

        lut = []
        bin_length = self.color_depth // bins_num
        bins_range = [i * bin_length for i in range(bins_num)]

        for i in range(bins_num - 1):
            lut.extend([bins_range[i]] * bin_length)

        # Fill the last bin range up to color depth with a maximum pixel value
        lut.extend([self.color_depth - 1] * (self.color_depth - bins_range[-1]))

        return lut

    def update_bins_value(self):
        """Update :attr:`label_bins_num` whenever is changed."""

        self.label_bins_num.setText("Posterize Bins Number: "
                                    + str(self.bins_slider.value()))

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate image posterization based on slider value.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        bins_num = self.bins_slider.value()
        lut = self.calc_posterize_lut(bins_num)

        self.current_img_data = self.__apply_lut(lut)
        super().update_img_preview()
