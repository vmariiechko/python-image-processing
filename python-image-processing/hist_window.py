import matplotlib

from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = figure.add_subplot(111)
        super(MplCanvas, self).__init__(figure)


class HistSubWindow(QMdiSubWindow):

    def __init__(self, *args, **kwargs):
        super(HistSubWindow, self).__init__(*args, **kwargs)

    def create_histogram_plot(self, hist, img_name):
        sc = MplCanvas(self)

        for i, col in enumerate(hist[1]):
            sc.axes.plot(range(256), hist[0][i], color=col)

        toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        widget = QWidget()
        widget.setLayout(layout)

        self.setWidget(widget)
        self.setWindowTitle("Histogram of " + img_name)
