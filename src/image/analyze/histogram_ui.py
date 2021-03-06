from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
                             QTableWidget, QTableWidgetItem, QAbstractItemView)
from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib import use

use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):
    """Build base canvas for plotting."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Create the center figure for plotting.

        :param width: The width of the figure in inches
        :type width: int
        :param height: The height of the figure in inches
        :type height: int
        :param dpi: The number of pixels that the figure comprises
        :type dpi: int
        """

        figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = figure.add_subplot(111)
        super(MplCanvas, self).__init__(figure)


class HistGraphicalUI:
    """Build UI for :class:`hist_window.HistGraphical`."""

    def init_ui(self, hist_sub_window):
        """
        Create user interface for :class:`hist_window.HistGraphical`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param hist_sub_window: The window for graphical representation of histogram
        :type hist_sub_window: :class:`hist_window.HistGraphical`
        """

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/histogram.png"), QIcon.Normal, QIcon.Off)
        hist_sub_window.setWindowIcon(icon)

        self.hist_canvas = MplCanvas(hist_sub_window)
        self.hist_canvas.setObjectName("hist_canvas")

        self.toolbar = NavigationToolbar(self.hist_canvas, self)
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
        self.layout.addWidget(self.hist_canvas)
        self.layout.addLayout(self.horizontal_layout)

        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.widget.setLayout(self.layout)

        hist_sub_window.setWidget(self.widget)
        QMetaObject.connectSlotsByName(hist_sub_window)


class HistListUI:
    """Build UI for :class:`hist_window.HistList`."""

    def init_ui(self, hist_sub_window, row_count):
        """
        Create user interface for :class:`hist_window.HistList`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param hist_sub_window: The window for list representation of histogram
        :type hist_sub_window: :class:`hist_window.HistList`
        :param row_count: The number of rows in list
        :type row_count: int
        """

        hist_sub_window.resize(239, 407)

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/table.png"), QIcon.Normal, QIcon.Off)
        hist_sub_window.setWindowIcon(icon)

        self.table_widget = QTableWidget()
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(row_count)

        for i in range(row_count):
            self.table_widget.setVerticalHeaderItem(i, QTableWidgetItem())

        item = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, item)

        item = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, item)

        hist_sub_window.setWidget(self.table_widget)
