from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMdiSubWindow, QTableWidgetItem

from hist_window_ui import HistGraphicalUI, HistListUI


class HistGraphical(QMdiSubWindow, HistGraphicalUI):

    def __init__(self, *args, **kwargs):
        super(HistGraphical, self).__init__(*args, **kwargs)

    def __retranslate_ui(self, img_name):
        _translate = QCoreApplication.translate

        self.setWindowTitle("Histogram plot of " + img_name)
        self.btn_list.setText(_translate("Histogram of " + img_name, "List"))
        self.btn_red.setText(_translate("Histogram of " + img_name, "Red"))
        self.btn_green.setText(_translate("Histogram of " + img_name, "Green"))
        self.btn_blue.setText(_translate("Histogram of " + img_name, "Blue"))
        self.btn_rgb.setText(_translate("Histogram of " + img_name, "R + G + B"))

    def __show_all_channels(self, hist):
        self.current_channel = 'rgb'

        self.hist_plot.axes.clear()
        for col in self.current_channel:
            self.hist_plot.axes.plot(range(256), hist[col], color=col)
        self.hist_plot.draw()

        if not self.histogram_list.isHidden():
            self.__show_histogram_list(hist)

    def __show_single_channel(self, hist, col):
        self.current_channel = col

        self.hist_plot.axes.clear()
        self.hist_plot.axes.plot(range(256), hist[col], color=col)
        self.hist_plot.draw()

        if not self.histogram_list.isHidden():
            self.__show_histogram_list(hist)

    def __show_histogram_list(self, hist, img_name=None):
        if len(self.current_channel) < 3:
            self.histogram_list.create_histogram_list(hist[self.current_channel], img_name)
        else:
            # Calculate maximum value for every pixel among all channels
            max_channels_values = [max(i) for i in zip(*hist.values())]
            self.histogram_list.create_histogram_list(max_channels_values, img_name)

        self.histogram_list.show()

    # Disable changing-channel buttons for grayscale image
    def __disable_channel_buttons(self):
        self.btn_red.setEnabled(False)
        self.btn_green.setEnabled(False)
        self.btn_blue.setEnabled(False)
        self.btn_rgb.setEnabled(False)

    def create_histogram_plot(self, hist, img_name):
        self.init_ui(self)
        self.histogram_list = HistList()

        self.btn_list.pressed.connect(lambda: self.__show_histogram_list(hist, img_name))
        self.btn_red.pressed.connect(lambda: self.__show_single_channel(hist, 'r'))
        self.btn_green.pressed.connect(lambda: self.__show_single_channel(hist, 'g'))
        self.btn_blue.pressed.connect(lambda: self.__show_single_channel(hist, 'b'))
        self.btn_rgb.pressed.connect(lambda: self.__show_all_channels(hist))

        if len(hist) < 3:
            self.__show_single_channel(hist, 'b')
            self.__disable_channel_buttons()
        else:
            self.__show_all_channels(hist)

        self.__retranslate_ui(img_name)


class HistList(QMdiSubWindow, HistListUI):

    def __init__(self, *args, **kwargs):
        super(HistList, self).__init__(*args, **kwargs)

    def create_histogram_list(self, hist, img_name):
        if img_name:
            self.setWindowTitle("Histogram list of " + img_name)

        self.init_ui(self, len(hist))

        value_header = self.table_widget.horizontalHeaderItem(0)
        value_header.setText("Value")
        count_header = self.table_widget.horizontalHeaderItem(1)
        count_header.setText("Count")

        for value, count in enumerate(hist):
            self.table_widget.setItem(value, 0, QTableWidgetItem(str(value)))
            self.table_widget.setItem(value, 1, QTableWidgetItem(str(count)))
