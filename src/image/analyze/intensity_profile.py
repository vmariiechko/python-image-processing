from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMdiSubWindow

from .intensity_profile_ui import IntensityProfileUI


class IntensityProfile(QMdiSubWindow, IntensityProfileUI):
    """The IntensityProfile class implements a graphical representation of the profile line."""

    def __init__(self, title, *args, **kwargs):
        """Create class instance and set :attr:`window_is_closed` to ``True``."""

        super(IntensityProfile, self).__init__(*args, **kwargs)
        self.window_is_closed = True
        self._title = title

    def __retranslate_ui(self):
        """Set the text title of the widgets."""

        _translate = QCoreApplication.translate

        self.setWindowTitle("Profile plot of " + self._title)

    def set_title(self, title):
        """
        Set the intensity profile window title.

        :param title: The new title
        """

        self._title = title
        self.setWindowTitle("Profile plot of " + title)

    def __calc_line_points(self, p1, p2):
        """
        Calculate all the line points from :attr:`p1` to :attr:`p2`.

        :param p1: The start point of the profile line
        :type p1: :class:`.PyQt5.QtCore.QPoint`
        :param p2: The end point of the profile line
        :type p2: :class:`.PyQt5.QtCore.QPoint`
        """

        x1, x2 = p1.x(), p2.x()
        y1, y2 = p1.y(), p2.y()

        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)

        sign_x = 1 if x1 < x2 else -1
        sign_y = 1 if y1 < y2 else -1

        error = delta_x - delta_y
        self.line_points = []

        while x1 != x2 or y1 != y2:
            self.line_points.append([x1, y1])
            error2 = error*2

            if error2 > -delta_y:
                error -= delta_y
                x1 += sign_x

            if error2 < delta_x:
                error += delta_x
                y1 += sign_y

        self.line_points.append([x2, y2])

    def create_profile(self, points, img_data):
        """
        Create intensity profile window.

        Calculate pixel intensities between two :attr:`points`.

        - For one-channel image the intensities are the same as original.
        - For three-channel image the intensities are calculated using the formula: 0.24*R + 0.69*G + 0.07*B.

        Clear a previous plot.
        Plot and draw the intensities data.

        :param points: The begin-end point of the drawn profile line
        :type points: list[:class:`.PyQt5.QtCore.QPoint`, :class:`.PyQt5.QtCore.QPoint`]
        :param img_data: The image data. Taken from cv2.imread
        :type img_data: :class:`numpy.ndarray`
        """

        if self.window_is_closed:
            self.init_ui(self)
            self.window_is_closed = False

        self.__calc_line_points(points[0], points[1])

        intensities = [img_data[y][x] for x, y in self.line_points]

        if len(img_data.shape) == 3:
            intensities = [0.24 * r + 0.69 * g + 0.07 * b for b, g, r in intensities]

        self.profile_canvas.axes.clear()
        self.profile_canvas.axes.set_title("Zoom off the image to be able to draw a line on it", fontsize=10)
        self.profile_canvas.axes.plot(range(len(intensities)), intensities, color="black")
        self.profile_canvas.axes.set_xlabel("Distance (pixels)")
        self.profile_canvas.axes.set_ylabel("Gray Value")
        self.profile_canvas.draw()

        self.__retranslate_ui()

    def closeEvent(self, event):
        """Mark close event by setting :attr:`window_is_closed` to ``True``."""

        self.window_is_closed = True
        super(IntensityProfile, self).closeEvent(event)
