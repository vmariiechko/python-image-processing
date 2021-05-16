from cv2 import normalize, cvtColor, error, NORM_MINMAX
from numpy import abs
from PyQt5.QtWidgets import QMdiSubWindow, QLabel
from PyQt5.QtCore import Qt, QPoint, QEvent, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QPixmap, QIcon, QImage

from src.constants import BYTES_PER_PIXEL_2_BW_FORMAT, COLOR_CONVERSION_CODES
from .analyze import HistGraphical, IntensityProfile
from .modify import Rename
from operations.point import Normalize, Posterize, ImageCalculator
from operations.local import Smooth, EdgeDetection, DirectionalEdgeDetection, Sharpen, Convolve, Morphology
from operations.segmentation import Threshold, Watershed


class Image:
    """The Image class represents the image."""

    # Map operations name to their dialog windows
    DIALOG_OPERATIONS = {
        "normalize": Normalize,
        "posterize": Posterize,
        "smooth": Smooth,
        "edge_dt": EdgeDetection,
        "edge_dt_dir": DirectionalEdgeDetection,
        "sharpen": Sharpen,
        "convolve": Convolve,
        "morphology": Morphology,
        "threshold": Threshold,
        "watershed": Watershed,
    }

    def __init__(self, img_data, img_name):
        """
        Create a new image.

        :param img_data: The image data.
        :type img_data: :class:`numpy.ndarray`
        :param img_name: The name for an image
        :type img_name: str
        """

        # Convert BGRA image to BGR
        try:
            if img_data.shape[2] == 4:
                img_data = cvtColor(img_data, COLOR_CONVERSION_CODES["BGRA2BGR"])
        except LookupError:
            pass
        except error:
            pass

        self.data = img_data
        self.subwindow = ImageWindow(img_data, img_name)
        self.name = img_name
        self.histogram_graphical = HistGraphical(img_name)
        self.histogram_subwindows_added = False
        self.profile_subwindow_added = False

        self.__calc_color_depth()

    def __calc_color_depth(self):
        """Calculate color depth of image pixel."""

        self.color_depth = 2**(8 * self.data.dtype.itemsize)

    def __update_image_name(self, img_name):
        """
        Update an image name.

        :param img_name: The new image name
        :type img_name: str
        """

        self.name = img_name
        self.histogram_graphical.set_title(img_name)
        self.subwindow.set_title(img_name)

    def __calc_single_histogram(self):
        """
        Calculate the image histogram data for one channel.

        Count the number of pixels for each tonal value,
        iterating through one channel of the image.

        :return: The image histogram data: {channel_char: [number_of_pixels]}
        :rtype: dict[str, list[int]]
        """

        histogram = [0] * self.color_depth

        for w in range(self.data.shape[0]):
            for h in range(self.data.shape[1]):
                pixel = self.data[w][h]
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

        for w in range(self.data.shape[0]):
            for h in range(self.data.shape[1]):
                for i in range(self.data.shape[2]):
                    pixel = self.data[w][h][i]
                    histogram_rgb[i][pixel] += 1

        return {'b': histogram_rgb[0], 'g': histogram_rgb[1], 'r': histogram_rgb[2]}

    def __apply_lut(self, lut):
        """
        Apply LUT to the image.

        :param lut: The Lookup Table
        :type lut: list[int]
        """

        if self.is_grayscale():
            for w in range(self.data.shape[0]):
                for h in range(self.data.shape[1]):
                    self.data[w][h] = lut[self.data[w][h]]
        else:
            for w in range(self.data.shape[0]):
                for h in range(self.data.shape[1]):
                    for i in range(self.data.shape[2]):
                        self.data[w][h][i] = lut[self.data[w][h][i]]

    def update(self):
        """Update image graphical elements such as image window, histogram, etc."""

        self.__calc_color_depth()
        self.subwindow.set_img_data(self.data)

        if self.histogram_graphical.window_is_opened:
            self.create_hist_window()

    def is_grayscale(self):
        """
        Check if the image is grayscale.

        ``True`` if the image has one channel, otherwise ``False``.

        :rtype: bool
        """

        return len(self.data.shape) == 2

    def change_type(self, img_type):
        """
        Change image data type.

        :param img_type: The new type
        :type img_type: str
        """

        self.change_color_depth_2_uint8()
        self.data = cvtColor(self.data, COLOR_CONVERSION_CODES[img_type])

    def change_color_depth_2_uint8(self):
        """Convert image data type to CV_U8 in case it isn't CV_8U."""

        if self.data.dtype.itemsize > 1:
            self.data = normalize(abs(self.data), None, 0, 255, NORM_MINMAX, dtype=0)

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
        Calculate cumulative histogram.

        :return: The cumulative histogram (empirical distribution)
        :rtype: list[int]
        """

        hist = self.calc_histogram()['b']

        cumulative_hist = [hist[0]]
        for i in hist[1:]:
            cumulative_hist.append(cumulative_hist[-1] + i)

        return cumulative_hist

    def create_hist_window(self):
        """Create a histogram plot window of the image."""

        self.histogram_graphical.create_histogram_plot(self.calc_histogram())

    def equalize_histogram(self):
        """
        Perform histogram equalization:

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

    def calc_negation(self):
        """Perform image negation."""

        lut = [self.color_depth - i - 1 for i in range(self.color_depth)]
        self.__apply_lut(lut)

    def rename(self):
        """Open rename dialog window to change the image name."""

        dialog_rename = Rename(self.name)

        if dialog_rename.exec():
            self.__update_image_name(dialog_rename.new_name)

    def run_operation_dialog(self, operation):
        """
        Execute specified operation dialog.

        All possible operations listed in :attr:`DIALOG_OPERATIONS`

        :param operation: The operation to execute
        :type operation: str
        """

        operation_dialog = self.DIALOG_OPERATIONS[operation](self)

        if operation_dialog.exec():
            self.data = operation_dialog.img_data

    @staticmethod
    def run_calculator_dialog(images):
        """
        Open calculator dialog window to perform double-argument point operation.

        :param images: The list of objects :class:`Image` to perform calculation
        :type images: list
        :return: The new image data and its name, tuple(data, img_name)
        :rtype: tuple or None
        """

        images = {img.name: img.data for img in images}
        calculator = ImageCalculator(images)

        if calculator.exec():
            return calculator.img_data, calculator.img_name


class ImageWindow(QMdiSubWindow):
    """The ImageWindow class implements image visualization in sub-window."""

    closed = pyqtSignal()

    def __init__(self, img_data, img_name, parent=None):
        """
        Create a new image sub-window.

        Create an empty :class:`intensity_profile.IntensityProfile` object.
        Load image to window. Set icon and window size.

        :param img_data: The image data.
        :type img_data: :class:`numpy.ndarray`
        :param img_name: The name of an image
        :type img_name: str
        """

        super().__init__(parent)

        self._data = img_data
        self.intensity_profile = IntensityProfile(img_name)
        self._title = img_name

        self.image_label = QLabel()
        self.pixmap = None
        self.update_window()
        self.update_icon()

        self.setFixedSize(self.pixmap.width() + 15, self.pixmap.height() + 35)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWidget(self.image_label)
        self.setWindowTitle(self._title)

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

        img_width = self._data.shape[1] - 1
        if point.x() > img_width:
            point.setX(img_width)

        img_height = self._data.shape[0] - 1
        if point.y() > img_height:
            point.setY(img_height)

        return point

    def _is_grayscale(self):
        """
        Check if the image is grayscale.

        ``True`` if the image has one channel, otherwise ``False``.

        :rtype: bool
        """

        return len(self._data.shape) == 2

    def set_img_data(self, img_data):
        """
        Set an image data and update the image window

        :param img_data: The image data to set
        :type img_data: :class:`numpy.ndarray`
        """

        self._data = img_data
        self.update_window()
        self.update_icon()

    def set_title(self, title):
        """
        Set an image window title.

        :param title: The new title
        """

        self._title = title
        self.intensity_profile.set_title(title)
        self.setWindowTitle(title)

    def update_window(self):
        """
        Update image sub-window.

        Convert image data to :class:`PyQt5.QtGui.QImage`.
        Load the image to the the sub-window.
        """

        height, width = self._data.shape[:2]

        if self._is_grayscale():
            pixel_bytes = self._data.dtype.itemsize
            image = QImage(self._data, width, height, BYTES_PER_PIXEL_2_BW_FORMAT[pixel_bytes])
        else:
            image = QImage(self._data, width, height, 3 * width, QImage.Format_BGR888)

        self.pixmap = QPixmap(image)
        self.image_label.setPixmap(self.pixmap.copy())

    def update_icon(self):
        """
        Update icon for image window.

        Grayscale image has grayscale picture, color image has color one.
        """

        icon = QIcon()
        if self._is_grayscale():
            icon.addPixmap(QPixmap("icons/picture_gray.png"), QIcon.Normal, QIcon.Off)
        else:
            icon.addPixmap(QPixmap("icons/picture_color.png"), QIcon.Normal, QIcon.Off)

        self.setWindowIcon(icon)

    def create_profile(self):
        """Create intensity profile window."""

        self.intensity_profile.create_profile(self.points, self._data)

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

    def closeEvent(self, event):
        """Filter the close event to emit signal :attr:`closed`."""

        super(ImageWindow, self).closeEvent(event)
        self.closed.emit()
