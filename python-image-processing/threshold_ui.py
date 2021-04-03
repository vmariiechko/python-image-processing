from PyQt5.QtWidgets import (QLabel, QSlider, QVBoxLayout, QDialogButtonBox,
                             QHBoxLayout, QRadioButton, QWidget)
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap


class ThresholdUI:
    """Build UI for :class:`threshold.Threshold`."""

    def init_ui(self, threshold):
        """
        Create user interface for :class:`threshold.Threshold`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param threshold: The dialog threshold window
        :type threshold: :class:`threshold.Threshold`
        """

        threshold.setObjectName("threshold")

        icon = QIcon()
        icon.addPixmap(QPixmap("images/threshold.png"), QIcon.Normal, QIcon.Off)
        threshold.setWindowIcon(icon)

        self.label_thresh_value = QLabel(threshold)
        self.label_thresh_value.setObjectName("label_thresh_value")
        self.label_thresh_value.setAlignment(Qt.AlignCenter)

        self.layout_rbtn = QHBoxLayout()
        self.layout_rbtn.setObjectName("layout_rbtn")

        self.rbtn_thresh_binary = QRadioButton("Threshold Binary")
        self.rbtn_thresh_binary.setObjectName("rbtn_thresh_binary")
        self.rbtn_thresh_binary.setLayoutDirection(Qt.RightToLeft)
        self.rbtn_thresh_binary.setChecked(True)

        self.rbtn_thresh_zero = QRadioButton("Threshold Zero")
        self.rbtn_thresh_zero.setObjectName("rbtn_thresh_zero")

        self.layout_rbtn.addWidget(self.rbtn_thresh_binary)
        self.layout_rbtn.addWidget(self.rbtn_thresh_zero)

        self.rbtn_group = QWidget(threshold)
        self.rbtn_group.setLayout(self.layout_rbtn)

        self.threshold_slider = QSlider(threshold)
        self.threshold_slider.setOrientation(Qt.Horizontal)
        self.threshold_slider.setObjectName("threshold_slider")

        self.label_image = QLabel(threshold)
        self.label_image.setObjectName("label_image")

        self.button_box = QDialogButtonBox(threshold)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(threshold.reject)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.label_thresh_value)
        self.layout.addWidget(self.rbtn_group)
        self.layout.addWidget(self.threshold_slider)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        threshold.setLayout(self.layout)
        threshold.setWindowFlags(threshold.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        QMetaObject.connectSlotsByName(threshold)
