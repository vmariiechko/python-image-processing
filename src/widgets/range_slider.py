from PyQt5.QtWidgets import (QWidget, QStyleOptionSlider, QSizePolicy,
                             QSlider, QStyle, QApplication)
from PyQt5.QtGui import QPainter, QPalette, QBrush
from PyQt5.QtCore import QRect, Qt, QSize, pyqtSignal


class RangeSlider(QWidget):
    """Class RangeSlider implements a double slider."""

    range_chagned = pyqtSignal()
    left_value_changed = pyqtSignal()
    right_value_changed = pyqtSignal()

    def __init__(self, color_depth, limits, parent=None):
        """
        Create a new range slider with :param:`color_depth` maximum value
        and slider :param:`limits`.

        :param color_depth: The maximum value for slider
        :type color_depth: int
        :param limits: The limits for sliders, list[left_limit, right_limit], including
        :type limits: list[int]
        """

        super().__init__(parent)

        self.first_position = 0
        self.second_position = color_depth - 1

        assert limits and limits[0] < limits[1], ValueError("Invalid limits")
        self.left_limit = limits[0]
        self.right_limit = limits[1]

        self.options = QStyleOptionSlider()
        self.options.minimum = 0
        self.options.maximum = color_depth - 1

        self.set_tick_position(QSlider.TicksAbove)
        self.set_tick_interval(color_depth // 8)

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed, QSizePolicy.Slider)
        )

    def set_tick_position(self, position):
        """
        Set a tick position.

        :param position: The position to set
        :type position: :class:`PyQt5.QtWidgets.QSlider.TickPosition`
        """

        self.options.tickPosition = position

    def set_tick_interval(self, interval):
        """
        Set a tick interval.

        :param interval: The interval to set
        :type interval: int
        """

        self.options.tickInterval = interval

    def paintEvent(self, event):
        """Draw the range slider objects."""

        painter = QPainter(self)

        # Rule
        self.options.initFrom(self)
        self.options.rect = self.rect()
        self.options.subControls = QStyle.SC_SliderGroove | QStyle.SC_SliderTickmarks

        # Groove
        self.style().drawComplexControl(QStyle.CC_Slider, self.options, painter)

        # Interval
        color = self.palette().color(QPalette.Highlight)
        color.setAlpha(150)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)

        self.options.sliderPosition = self.first_position
        left_handle = (
            self.style().subControlRect(
                QStyle.CC_Slider, self.options, QStyle.SC_SliderHandle
            ).right()
        )

        self.options.sliderPosition = self.second_position
        right_handle = (
            self.style().subControlRect(
                QStyle.CC_Slider, self.options, QStyle.SC_SliderHandle
            ).left()
        )

        groove_rect = self.style().subControlRect(
            QStyle.CC_Slider, self.options, QStyle.SC_SliderGroove
        )

        selection = QRect(
            left_handle,
            groove_rect.y(),
            right_handle - left_handle,
            groove_rect.height(),
        ).adjusted(-1, 1, 1, -1)

        painter.drawRect(selection)

        # Left handle
        self.options.subControls = QStyle.SC_SliderHandle
        self.options.sliderPosition = self.first_position
        self.style().drawComplexControl(QStyle.CC_Slider, self.options, painter)

        # Right handle
        self.options.sliderPosition = self.second_position
        self.style().drawComplexControl(QStyle.CC_Slider, self.options, painter)

    def mousePressEvent(self, event):
        """Filter a handle press."""

        self.options.sliderPosition = self.first_position
        self._first_sc = self.style().hitTestComplexControl(
            QStyle.CC_Slider, self.options, event.pos(), self
        )

        self.options.sliderPosition = self.second_position
        self._second_sc = self.style().hitTestComplexControl(
            QStyle.CC_Slider, self.options, event.pos(), self
        )

    def mouseMoveEvent(self, event):
        """
        Update the handle position.

        Depending on handle emit:

        - The :attr:`left_value_changed` for first handle.
        - The :attr:`right_value_changed` for second handle.
        """

        distance = self.options.maximum - self.options.minimum

        position = self.style().sliderValueFromPosition(
            0, distance, event.pos().x(), self.rect().width()
        )

        if self._first_sc == QStyle.SC_SliderHandle:
            if position <= self.left_limit:
                self.first_position = position
                self.left_value_changed.emit()
                self.update()
                return

        if self._second_sc == QStyle.SC_SliderHandle:
            if position >= self.right_limit:
                self.second_position = position
                self.right_value_changed.emit()
                self.update()

    def mouseReleaseEvent(self, event):
        """Emit the :attr:`range_changed` signal."""

        if QStyle.SC_SliderHandle in [self._first_sc, self._second_sc]:
            self.range_chagned.emit()

    def sizeHint(self):
        """Set recommended size for the range slider."""

        slider_len = 100
        tick_space = 7

        width = slider_len
        height = self.style().pixelMetric(QStyle.PM_SliderThickness, self.options, self)

        if (self.options.tickPosition & QSlider.TicksAbove
                or self.options.tickPosition & QSlider.TicksBelow):
            height += tick_space

        return self.style().sizeFromContents(
            QStyle.CT_Slider, self.options, QSize(width, height), self
        ).expandedTo(QApplication.globalStrut())
