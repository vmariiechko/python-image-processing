import matplotlib

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QMetaObject

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = figure.add_subplot(111)
        super(MplCanvas, self).__init__(figure)


class HistGraphicalSubWindowUI:
    def init_ui(self, hist_sub_window):

        self.sc_plot = MplCanvas(hist_sub_window)
        self.sc_plot.setObjectName("sc_plot")

        self.toolbar = NavigationToolbar(self.sc_plot, self)
        self.toolbar.setObjectName("toolbar")

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")

        self.btn_list = QPushButton(self)
        self.btn_list.setObjectName("btn_list")

        self.btn_red = QPushButton(self)
        self.btn_red.setObjectName("btn_red")
        self.btn_red.setAutoDefault(True)

        self.btn_green = QPushButton(self)
        self.btn_green.setObjectName("btn_green")
        self.btn_green.setAutoDefault(True)

        self.btn_blue = QPushButton(self)
        self.btn_blue.setObjectName("btn_blue")
        self.btn_blue.setAutoDefault(True)

        self.btn_rgb = QPushButton(self)
        self.btn_rgb.setObjectName("btn_rgb")
        self.btn_rgb.setAutoDefault(True)

        self.horizontal_layout.addWidget(self.btn_list)
        self.horizontal_layout.addWidget(self.btn_red)
        self.horizontal_layout.addWidget(self.btn_green)
        self.horizontal_layout.addWidget(self.btn_blue)
        self.horizontal_layout.addWidget(self.btn_rgb)

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.sc_plot)
        self.layout.addLayout(self.horizontal_layout)

        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.widget.setLayout(self.layout)

        hist_sub_window.setWidget(self.widget)
        QMetaObject.connectSlotsByName(hist_sub_window)
