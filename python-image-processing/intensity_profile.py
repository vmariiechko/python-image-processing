from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMdiSubWindow

from intensity_profile_ui import IntensityProfileUI


class IntensityProfile(QMdiSubWindow, IntensityProfileUI):

    def __init__(self, *args, **kwargs):
        super(IntensityProfile, self).__init__(*args, **kwargs)
        self.window_is_closed = True

    def __retranslate_ui(self, img_name):
        _translate = QCoreApplication.translate

        self.setWindowTitle("Profile plot of " + img_name)

    def __calc_line_points(self, p1, p2):
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

    def create_profile(self, points, image, img_name):

        if self.window_is_closed:
            self.init_ui(self)
            self.window_is_closed = False

        self.__calc_line_points(points[0], points[1])

        intensities = [image[y][x] for x, y in self.line_points]

        if len(image.shape) == 3:
            intensities = [0.24 * r + 0.69 * g + 0.07 * b for b, g, r in intensities]

        self.profile_canvas.axes.clear()
        self.profile_canvas.axes.plot(range(len(intensities)), intensities, color="black")
        self.profile_canvas.axes.set_xlabel("Distance (pixels)")
        self.profile_canvas.axes.set_ylabel("Gray Value")
        self.profile_canvas.draw()

        self.__retranslate_ui(img_name)

    def closeEvent(self, event):
        self.window_is_closed = True
        super(IntensityProfile, self).closeEvent(event)
