from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from histogram_ui import MplCanvas
from range_slider import RangeSlider


class NormalizeUI:
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

        normalize.setObjectName("normalize")

        icon = QIcon()
        icon.addPixmap(QPixmap("images/normalize.png"), QIcon.Normal, QIcon.Off)
        normalize.setWindowIcon(icon)

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

        self.button_box = QDialogButtonBox(normalize)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(normalize.reject)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.label_txt)
        self.layout.addWidget(self.hist_canvas)
        self.layout.addWidget(self.slider_widget)
        self.layout.addWidget(self.button_box)

        normalize.setLayout(self.layout)
        normalize.setWindowFlags(normalize.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        QMetaObject.connectSlotsByName(normalize)
