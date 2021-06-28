from PyQt5.QtWidgets import QDialog

from ..operation import Operation
from .normalize_ui import NormalizeUI


class Normalize(QDialog, Operation, NormalizeUI):
    """The Normalize class impelements a histogram normalization."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform normalization.

        :param parent: The image to normalize
        :type parent: :class:`image.Image`
        """

        super().__init__()

        self.color_depth = parent.color_depth
        self.original_hist = parent.calc_histogram()['b']
        self.img_data = parent.data.copy()
        self.current_img_data = None

        self.init_ui(self, [self.img_data.min(), self.img_data.max()])
        self.label_txt.setText("Choose the range for normalization:")
        self.setWindowTitle("Normalize")

        self.range_slider.left_value_changed.connect(self.update_left_value)
        self.range_slider.right_value_changed.connect(self.update_right_value)
        self.range_slider.range_chagned.connect(self.update_plot_preview)

        self.update_left_value()
        self.update_right_value()
        self.update_plot_preview()

    def calc_histogram(self, img_data):
        """
        Calculate image histogram data.

        :param img_data: The image data to calculate histogram
        :type img_data: :class:`numpy.ndarray`
        :return: The histogram data
        :rtype: list
        """

        histogram = [0] * self.color_depth

        for w in range(img_data.shape[0]):
            for h in range(img_data.shape[1]):
                pixel = img_data[w][h]
                histogram[pixel] += 1

        return histogram

    def normalize_histogram(self, min_val, max_val):
        """
        Calculate histogram normalization:

        - Define min/max pixel values in the image.
        - Calculate contrast stretching for range: [:attr:`min_val`; :attr:`max_val`]

        :param min_val: The lower stretching bound
        :type min_val: int
        :param max_val: The upper stretching bound
        :type max_val: int
        :return: The new updated image data
        :rtype: class:`numpy.ndarray`
        """

        img_data = self.img_data.copy()

        img_min = img_data.min()
        img_max = img_data.max()

        for w in range(img_data.shape[0]):
            for h in range(img_data.shape[1]):
                # Linear transformation
                img_data[w][h] = min_val + (img_data[w][h] - img_min) * (max_val - min_val)/(img_max - img_min)

        return img_data

    def update_left_value(self):
        """Update :attr:`label_left_value` whenever is changed."""

        self.label_left_value.setText(str(self.range_slider.first_position))

    def update_right_value(self):
        """Update :attr:`label_right_value` whenever is changed."""

        self.label_right_value.setText(str(self.range_slider.second_position))

    def update_plot_preview(self):
        """
        Update histogram preview window.

        Calculate image normalization based on slider range.
        Draw original and normalized histogram.
        """

        min_val = self.range_slider.first_position
        max_val = self.range_slider.second_position
        img_data = self.normalize_histogram(min_val, max_val)
        new_hist = self.calc_histogram(img_data)

        self.hist_canvas.axes.clear()
        self.hist_canvas.axes.bar(range(256), self.original_hist, color='b', alpha=0.7)
        self.hist_canvas.axes.bar(range(256), new_hist, color='g', alpha=0.7)
        self.hist_canvas.draw()

        self.current_img_data = img_data
