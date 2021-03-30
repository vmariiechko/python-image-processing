from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMdiSubWindow, QTableWidgetItem

from hist_window_ui import HistGraphicalUI, HistListUI


class HistGraphical(QMdiSubWindow, HistGraphicalUI):
    """The HistGraphical class implements a graphical representation of the image histogram."""

    def __init__(self, img_name, *args, **kwargs):
        """Create a new histogram graphical representation and :class:`HistList` instance."""

        super(HistGraphical, self).__init__(*args, **kwargs)

        self.histogram_list = HistList(img_name)
        self.img_name = img_name
        self.window_is_opened = False

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate

        self.setWindowTitle("Histogram plot of " + self.img_name)
        self.btn_list.setText(_translate("Histogram of " + self.img_name, "List"))
        self.btn_red.setText(_translate("Histogram of " + self.img_name, "Red"))
        self.btn_green.setText(_translate("Histogram of " + self.img_name, "Green"))
        self.btn_blue.setText(_translate("Histogram of " + self.img_name, "Blue"))
        self.btn_rgb.setText(_translate("Histogram of " + self.img_name, "R + G + B"))

    def __show_all_channels(self, hist):
        """
        Create a plot for three channels.

        Clear a previous plot.
        Plot and draw the histogram data.
        Calculate a histogram list representation when the list window is open.

        :param hist: The histogram data of the image. Taken from :meth:`image.Image.calc_histogram`
                     {channel_char: [number_of_pixels]}
        :type hist: dict[str, list[int]]
        """

        self.current_channel = 'rgb'

        self.hist_canvas.axes.clear()
        for col in self.current_channel:
            self.hist_canvas.axes.plot(range(256), hist[col], color=col)
        self.hist_canvas.draw()

        if not self.histogram_list.isHidden():
            self.__show_histogram_list(hist)

    def __show_single_channel(self, hist, col):
        """
        Create a plot for a single channel.

        Clear a previous plot.
        Plot and draw the histogram data.
        Calculate a histogram list representation when the list window is open.

        :param hist: The histogram data of the image. Taken from :meth:`image.Image.calc_histogram`
                     {channel_char: [number_of_pixels]}
        :type hist: dict[str, list[int]]
        :param col: The color of plot line
        :type col: str
        """

        self.current_channel = col

        self.hist_canvas.axes.clear()
        self.hist_canvas.axes.plot(range(256), hist[col], color=col)
        self.hist_canvas.draw()

        if not self.histogram_list.isHidden():
            self.__show_histogram_list(hist)

    def __show_histogram_list(self, hist):
        """
        Create a histogram list of the image.

        Depending on the number of channels, calculate the histogram list:

        - for a grayscale image, taking its original channel data;
        - for a color image, taking the maximum number of pixels for every tonal value among channels.

        :param hist: The histogram data of the image. Taken from :meth:`image.Image.calc_histogram`
                     {channel_char: [number_of_pixels]}
        :type hist: dict[str, list[int]]
        """

        if len(self.current_channel) < 3:
            self.histogram_list.create_histogram_list(hist[self.current_channel])
        else:
            # Calculate maximum value for every pixel among all channels
            max_channels_values = [max(i) for i in zip(*hist.values())]
            self.histogram_list.create_histogram_list(max_channels_values)

        self.histogram_list.show()

    def __disable_channel_buttons(self):
        """Disable changing-channel buttons for a grayscale image."""

        self.btn_red.setEnabled(False)
        self.btn_green.setEnabled(False)
        self.btn_blue.setEnabled(False)
        self.btn_rgb.setEnabled(False)

    def create_histogram_plot(self, hist):
        """
        Create a histogram plot of the image.

        Initialize user interface.
        Connect list and changing-channel buttons.
        Create a histogram for grayscale or color image.

        :param hist: The histogram data of the image. Taken from :meth:`image.Image.calc_histogram`
                     {channel_char: [number_of_pixels]}
        :type hist: dict[str, list[int]]
        """

        self.init_ui(self)
        self.window_is_opened = True

        self.btn_list.pressed.connect(lambda: self.__show_histogram_list(hist))
        self.btn_red.pressed.connect(lambda: self.__show_single_channel(hist, 'r'))
        self.btn_green.pressed.connect(lambda: self.__show_single_channel(hist, 'g'))
        self.btn_blue.pressed.connect(lambda: self.__show_single_channel(hist, 'b'))
        self.btn_rgb.pressed.connect(lambda: self.__show_all_channels(hist))

        if len(hist) < 3:
            self.__show_single_channel(hist, 'b')
            self.__disable_channel_buttons()
        else:
            self.__show_all_channels(hist)

        self.__retranslate_ui()

    def closeEvent(self, event):
        """Mark close event by setting :attr:`window_is_opened` to ``False``."""

        self.window_is_opened = False
        super(HistGraphical, self).closeEvent(event)


class HistList(QMdiSubWindow, HistListUI):
    """The HistList class implements a list representation of the image histogram."""

    def __init__(self, img_name, *args, **kwargs):
        """Create a new histogram list representation."""

        super(HistList, self).__init__(*args, **kwargs)
        self.img_name = img_name

    def create_histogram_list(self, hist):
        """
        Create a histogram list of the image.

        Initialize user interface.
        Create a table with two columns:

        - pixel value;
        - number of pixels.

        :param hist: The histogram data of the image without specifying channel
        :type hist: list[int]
        """

        self.setWindowTitle("Histogram list of " + self.img_name)

        self.init_ui(self, len(hist))

        value_header = self.table_widget.horizontalHeaderItem(0)
        value_header.setText("Value")
        count_header = self.table_widget.horizontalHeaderItem(1)
        count_header.setText("Count")

        for value, count in enumerate(hist):
            self.table_widget.setItem(value, 0, QTableWidgetItem(str(value)))
            self.table_widget.setItem(value, 1, QTableWidgetItem(str(count)))
