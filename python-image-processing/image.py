from PyQt5.QtWidgets import QMdiSubWindow, QLabel
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QPainter, QPen, QPixmap, QIcon

from hist_window import HistGraphical
from intensity_profile import IntensityProfile


class Image:
    def __init__(self, img_data, path):
        self.image = img_data
        self.img_window = ImageWindow(img_data, path)
        self.img_name = path.split("/")[-1]
        self.histogram_graphical = HistGraphical()

    def __calc_single_histogram(self):
        histogram = [0] * 256

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                pixel = self.image[w][h]
                histogram[pixel] += 1

        return {'b': histogram}

    def __calc_triple_histogram(self):
        histogram_rgb = [[0] * 256, [0] * 256, [0] * 256]

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                for i in range(self.image.shape[2]):
                    pixel = self.image[w][h][i]
                    histogram_rgb[i][pixel] += 1

        return {'b': histogram_rgb[0], 'g': histogram_rgb[1], 'r': histogram_rgb[2]}

    def calc_histogram(self):
        if len(self.image.shape) == 2:
            return self.__calc_single_histogram()
        else:
            return self.__calc_triple_histogram()

    def create_hist_window(self):
        hist = self.calc_histogram()
        self.histogram_graphical.create_histogram_plot(hist, self.img_name)


class ImageWindow(QMdiSubWindow):

    def __init__(self, img_data, path, parent=None):
        super().__init__(parent)

        self.image = img_data
        self.intensity_profile = IntensityProfile()
        self.img_name = path.split("/")[-1]

        self.image_label = QLabel()
        self.pixmap = QPixmap(path)
        self.image_label.setPixmap(self.pixmap.copy())
        self.resize(self.pixmap.width() + 15, self.pixmap.height() + 35)

        icon = QIcon()
        icon.addPixmap(QPixmap("images/picture.png"), QIcon.Normal, QIcon.Off)

        self.setWidget(self.image_label)
        self.setWindowTitle(self.img_name)
        self.setWindowIcon(icon)

        self.points = [QPoint(0, 0), QPoint(0, 0)]
        self.drawing = False

    def eventFilter(self, obj, event):
        event_type = event.type()

        if event_type == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.points[0] = event.pos()
                self.image_label.setPixmap(self.pixmap.copy())
                self.drawing = True

        elif event_type == QEvent.MouseMove and self.drawing:
            self.points[1] = event.pos()
            self.image_label.setPixmap(self.pixmap.copy())

            painter = QPainter(self.image_label.pixmap())
            painter.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
            painter.drawLine(self.points[0], self.points[1])

            self.update()

        elif event_type == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self.points[1] = event.pos()
                self.drawing = False
                self.create_profile()

        return super(ImageWindow, self).eventFilter(obj, event)

    def create_profile(self):
        self.intensity_profile.create_profile(self.points, self.image, self.img_name)
