from PyQt5.QtWidgets import QMdiSubWindow, QLabel
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QPainter, QPen, QPixmap, QIcon, QImage

from hist_window import HistGraphical
from intensity_profile import IntensityProfile


class Image:
    """The Image class represents the image."""

    def __init__(self, img_data, path):
        """
        Create a new image.

        :param img_data: The image data. Taken from cv2.imread
        :type img_data: :class:`numpy.ndarray`
        :param path: The path to the image
        :type path: str
        """

        self.image = img_data
        self.img_window = ImageWindow(img_data, path)
        self.img_name = path.split("/")[-1]
        self.histogram_graphical = HistGraphical(self.img_name)

    def __calc_single_histogram(self):
        """
        Calculate the image histogram data for one channel.

        Count the number of pixels for each tonal value,
        iterating through one channel of the image.

        :return: The image histogram data: {channel_char: [number_of_pixels]}
        :rtype: dict[str, list[int]]
        """

        histogram = [0] * 256

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                pixel = self.image[w][h]
                histogram[pixel] += 1

        return {'b': histogram}

    def __calc_triple_histogram(self):
        """
        Calculate the image histogram data for three channels.

        Count the number of pixels for each tonal value,
        iterating through three channels of the image.

        :return: The image histogram data: {channel_char: [number_of_pixels]}
        :rtype: dict[str, list[int]]
        """

        histogram_rgb = [[0] * 256, [0] * 256, [0] * 256]

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                for i in range(self.image.shape[2]):
                    pixel = self.image[w][h][i]
                    histogram_rgb[i][pixel] += 1

        return {'b': histogram_rgb[0], 'g': histogram_rgb[1], 'r': histogram_rgb[2]}

    def update(self):
        self.img_window.update_window(self.image)

        if self.histogram_graphical.window_is_opened:
            self.create_hist_window()

    def is_grayscale(self):
        return len(self.image.shape) == 2

    def calc_histogram(self):
        """
        Calculate image histogram data.

        Depending on the number of channels, calculate histogram:

        - for grayscale image using :meth:`__calc_single_histogram`;
        - for color iamge using :meth:`__calc_triple_histogram`.

        :return: The image histogram data for every channel: {channel_char: [number_of_pixels]}
        :rtype: dict[str, list[int]]
        """

        if self.is_grayscale():
            return self.__calc_single_histogram()
        else:
            return self.__calc_triple_histogram()

    def create_hist_window(self):
        """Create a histogram plot window of the image."""

        self.histogram_graphical.create_histogram_plot(self.calc_histogram())

    def normalize_histogram(self):
        img_min = self.image.min()
        img_max = self.image.max()

        min_val = 0
        max_val = 255

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                self.image[w][h] = ((self.image[w][h] - img_min) * max_val) / (img_max - img_min)


class ImageWindow(QMdiSubWindow):
    """The ImageWindow class implements image visualization in sub-window."""

    def __init__(self, img_data, path, parent=None):
        """
        Create a new image sub-window.

        Create an empty :class:`intensity_profile.IntensityProfile` object.
        Load image to window. Set icon and window size.

        :param img_data: The image data. Taken from cv2.imread
        :type img_data: :class:`numpy.ndarray`
        :param path: The path to the image
        :type path: str
        """

        super().__init__(parent)

        self.image = img_data
        self.intensity_profile = IntensityProfile()
        self.img_name = path.split("/")[-1]

        self.image_label = QLabel()
        self.pixmap = QPixmap(path)
        self.image_label.setPixmap(self.pixmap.copy())

        icon = QIcon()
        icon.addPixmap(QPixmap("images/picture.png"), QIcon.Normal, QIcon.Off)

        self.setFixedSize(self.pixmap.width() + 15, self.pixmap.height() + 35)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWidget(self.image_label)
        self.setWindowTitle(self.img_name)
        self.setWindowIcon(icon)

        self.points = [QPoint(0, 0), QPoint(0, 0)]
        self.drawing = False

    def __validate_point(self, point):
        """
        Validate the given point.

        Make sure point coordinates aren't beyond the corners of the image.

        :param point: The point of coordinates on image
        :type point: :class:`.PyQt5.QtCore.QPoint`
        :return: The validated point, which doesn't exceed the corners
        :rtype: :class:`.PyQt5.QtCore.QPoint`
        """

        if point.x() < 0:
            point.setX(0)

        if point.y() < 0:
            point.setY(0)

        img_width = self.image.shape[1] - 1
        if point.x() > img_width:
            point.setX(img_width)

        img_height = self.image.shape[0] - 1
        if point.y() > img_height:
            point.setY(img_height)

        return point

    def update_window(self, img_data):
        self.image = img_data
        height, width = img_data.shape

        img = QImage(self.image, width, height, QImage.Format_Grayscale8)
        self.pixmap = QPixmap(img)
        self.image_label.setPixmap(self.pixmap.copy())

    def eventFilter(self, obj, event):
        """
        Filter mouse clicks.

        - If LMB is clicked, then save first point coordinates and start drawing.
        - If LMB is moved, then save second point coordinates and draw a line.
        - If LMB is released, then save second point coordinates and create a profile between points.

        :param obj: The event sender object.
        :type obj: :class:`.PyQt5.QtCore.QObject`
        :param event: The happened event.
        :type event: :class:`.PyQt5.QtCore.QEvent`
        """

        event_type = event.type()

        if event_type == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.points[0] = event.pos()
                self.image_label.setPixmap(self.pixmap.copy())
                self.drawing = True

        elif event_type == QEvent.MouseMove and self.drawing:
            self.points[1] = self.__validate_point(event.pos())
            self.image_label.setPixmap(self.pixmap.copy())

            painter = QPainter(self.image_label.pixmap())
            painter.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
            painter.drawLine(self.points[0], self.points[1])

            self.update()

        elif event_type == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self.points[1] = self.__validate_point(event.pos())
                self.drawing = False
                self.create_profile()

        return super(ImageWindow, self).eventFilter(obj, event)

    def create_profile(self):
        """Create intensity profile window."""

        self.intensity_profile.create_profile(self.points, self.image, self.img_name)
