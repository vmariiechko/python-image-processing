from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI
from image.analyze import MplCanvas
from widgets.range_slider import RangeSlider


class NormalizeUI(OperationUI):
    """Build UI for :class:`normalize.Normalize`."""

    def init_ui(self, normalize, limits):
        """
        Create user interface for :class:`normalize.Normalize`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param normalize: The dialog normalize window
        :type normalize: :class:`normalize.Normalize`
        :param limits: The limits for range slider
        :type limits: list[int, int]
        """

        self.operation_ui(self)
        normalize.setObjectName("normalize")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/normalize.png"), QIcon.Normal, QIcon.Off)
        normalize.setWindowIcon(icon)

        self.rbtn_show_hist.setVisible(False)

        self.label_txt = QLabel(normalize)
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setAlignment(Qt.AlignCenter)

        self.hist_canvas = MplCanvas(normalize, width=7, height=4)
        self.hist_canvas.setObjectName("hist_canvas")

        self.label_left_value = QLabel(normalize)
        self.label_left_value.setObjectName("label_left_value")
        self.label_left_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.label_right_value = QLabel(normalize)
        self.label_right_value.setObjectName("label_right_value")

        self.range_slider = RangeSlider(normalize.color_depth, limits)
        self.range_slider.setObjectName("range_slider")

        self.layout_slider = QHBoxLayout()
        self.layout_slider.setObjectName("layout_slider")

        self.layout_slider.addWidget(self.label_left_value)
        self.layout_slider.addWidget(self.range_slider)
        self.layout_slider.addWidget(self.label_right_value)

        self.layout_slider.setStretch(0, 91)
        self.layout_slider.setStretch(1, 492)
        self.layout_slider.setStretch(2, 74)

        self.slider_widget = QWidget(normalize)
        self.slider_widget.setObjectName("slider_widget")
        self.slider_widget.setLayout(self.layout_slider)

        self.layout.addWidget(self.label_txt)
        self.layout.addWidget(self.hist_canvas)
        self.layout.addWidget(self.slider_widget)
        self.layout.addWidget(self.button_box)

        normalize.setLayout(self.layout)
        QMetaObject.connectSlotsByName(normalize)
