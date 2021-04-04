from PyQt5.QtWidgets import QMdiSubWindow, QLabel
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QPainter, QPen, QPixmap, QIcon, QImage

from histogram import HistGraphical
from intensity_profile import IntensityProfile
from threshold import Threshold
from posterize import Posterize


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
        self.color_depth = 2**(8 * self.image.dtype.itemsize)
        self.histogram_graphical = HistGraphical(self.img_name)

    def __calc_single_histogram(self):
        """
        Calculate the image histogram data for one channel.

        Count the number of pixels for each tonal value,
        iterating through one channel of the image.

        :return: The image histogram data: {channel_char: [number_of_pixels]}
        :rtype: dict[str, list[int]]
        """

        histogram = [0] * self.color_depth

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

        histogram_rgb = [[0] * self.color_depth, [0] * self.color_depth, [0] * self.color_depth]

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                for i in range(self.image.shape[2]):
                    pixel = self.image[w][h][i]
                    histogram_rgb[i][pixel] += 1

        return {'b': histogram_rgb[0], 'g': histogram_rgb[1], 'r': histogram_rgb[2]}

    def __apply_lut(self, lut):
        """
        Apply LUT to the image.

        :param lut: The Lookup Table
        :type lut: list[int]
        """

        if self.is_grayscale():
            for w in range(self.image.shape[0]):
                for h in range(self.image.shape[1]):
                    self.image[w][h] = lut[self.image[w][h]]
        else:
            for w in range(self.image.shape[0]):
                for h in range(self.image.shape[1]):
                    for i in range(self.image.shape[2]):
                        self.image[w][h][i] = lut[self.image[w][h][i]]

    def update(self):
        """Update image graphical elements such as image window, histogram, etc."""

        self.img_window.update_window(self.image)

        if self.histogram_graphical.window_is_opened:
            self.create_hist_window()

    def is_grayscale(self):
        """
        Check if the image is grayscale.

        ``True`` if the image has one channel, otherwise ``False``.

        :rtype: bool
        """

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

    def calc_cumulative_histogram(self):
        """
        Calculate cumulative histogram, which equals to the empirical distribution of histogram.

        :return: The empirical distribution
        :rtype: list[int]
        """

        hist = self.calc_histogram()['b']

        empirical_distr = [hist[0]]
        for i in hist[1:]:
            empirical_distr.append(empirical_distr[-1] + i)

        return empirical_distr

    def create_hist_window(self):
        """Create a histogram plot window of the image."""

        self.histogram_graphical.create_histogram_plot(self.calc_histogram())

    def normalize_histogram(self):
        """
        Change the image, execute histogram normalization:

        - Define min/max values in the image.
        - Calculate contrast stretching.
        """

        img_min = self.image.min()
        img_max = self.image.max()

        # Scaling range
        min_val = 0
        max_val = 255

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                self.image[w][h] = ((self.image[w][h] - img_min) * max_val) / (img_max - img_min)

    def equalize_histogram(self):
        """
        Change the image, execute histogram equalization:

        - Calculate cumulative histogram.
        - Calculate LUT for equalization.
        - Apply LUT to the picture.
        """

        lut = []
        cumulative_hist = self.calc_cumulative_histogram()

        # Find min/max values in the cumulative histogram, excluding zero as a minimum
        ord_hist_values = sorted(set(cumulative_hist))
        hist_min = ord_hist_values[1]
        hist_max = ord_hist_values[-1]

        for i in cumulative_hist:
            # Normalize cumulative sum to 0-255 range
            equalized_val = abs(int(((i - hist_min) * 255) / (hist_max - hist_min)))
            lut.append(equalized_val)

        self.__apply_lut(lut)

    def negation(self):
        """Perform image negation."""

        lut = [self.color_depth - i - 1 for i in range(self.color_depth)]
        self.__apply_lut(lut)

    def threshold(self):
        threshold = Threshold(self)

        if threshold.exec():
            self.image = threshold.img_data

    def posterize(self):
        posterize = Posterize(self)

        if posterize.exec():
            self.image = posterize.img_data


class ImageWindow(QMdiSubWindow):
    """The ImageWindow class implements image visualization in sub-window."""

    # Map ndarray.dtype.itemsize to QImage bytes per pixel format for grayscale image
    bytes_per_pixel = {
        1: QImage.Format_Grayscale8,
        2: QImage.Format_Grayscale16
    }

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
        """
        Update image sub-window.

        Convert new image data to :class:`PyQt5.QtGui.QImage`.
        Reload the image to the the sub-window.

        :param img_data: The changed image data
        :type img_data: :class:`ndarray`
        """

        self.image = img_data
        height, width = img_data.shape[:2]

        if len(img_data.shape) == 2:
            color_depth = img_data.dtype.itemsize
            img = QImage(self.image, width, height, self.bytes_per_pixel[color_depth])
        else:
            img = QImage(self.image, width, height, 3*width, QImage.Format_RGB888)

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
            point = event.pos()

            if event.button() == Qt.LeftButton and point.y() > -1:
                self.points[0] = point
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
            if event.button() == Qt.LeftButton and self.drawing:
                self.points[1] = self.__validate_point(event.pos())
                self.drawing = False
                self.create_profile()

        return super(ImageWindow, self).eventFilter(obj, event)

    def create_profile(self):
        """Create intensity profile window."""

        self.intensity_profile.create_profile(self.points, self.image, self.img_name)
