from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMdiSubWindow

from hist_window_ui import HistGraphicalSubWindowUI


class HistGraphicalSubWindow(QMdiSubWindow, HistGraphicalSubWindowUI):

    def __init__(self, *args, **kwargs):
        super(HistGraphicalSubWindow, self).__init__(*args, **kwargs)

    def __retranslate_ui(self, img_name):
        _translate = QCoreApplication.translate

        self.setWindowTitle("Histogram of " + img_name)
        self.btn_list.setText(_translate("Histogram of " + img_name, "List"))
        self.btn_red.setText(_translate("Histogram of " + img_name, "Red"))
        self.btn_green.setText(_translate("Histogram of " + img_name, "Green"))
        self.btn_blue.setText(_translate("Histogram of " + img_name, "Blue"))
        self.btn_rgb.setText(_translate("Histogram of " + img_name, "R + G + B"))

    def __show_all_channels(self, hist):
        self.current_channel = 'rgb'

        self.sc_plot.axes.clear()
        for col in self.current_channel:
            self.sc_plot.axes.plot(range(256), hist[col], color=col)
        self.sc_plot.draw()

    def __show_single_channel(self, hist, col):
        self.current_channel = col

        self.sc_plot.axes.clear()
        self.sc_plot.axes.plot(range(256), hist[col], color=col)
        self.sc_plot.draw()

    def create_histogram_plot(self, hist, img_name):
        self.init_ui(self)
        self.__show_all_channels(hist)

        self.btn_list.pressed.connect(lambda: self.__create_histogram_list(hist, img_name))
        self.btn_red.pressed.connect(lambda: self.__show_single_channel(hist, 'r'))
        self.btn_green.pressed.connect(lambda: self.__show_single_channel(hist, 'g'))
        self.btn_blue.pressed.connect(lambda: self.__show_single_channel(hist, 'b'))
        self.btn_rgb.pressed.connect(lambda: self.__show_all_channels(hist))

        # Block changing-channel buttons if an image is grayscale
        if len(hist) < 3:
            self.btn_red.setEnabled(False)
            self.btn_green.setEnabled(False)
            self.btn_blue.setEnabled(False)
            self.btn_rgb.setEnabled(False)

        self.__retranslate_ui(img_name)

    def __create_histogram_list(self, hist, img_name):
        pass
