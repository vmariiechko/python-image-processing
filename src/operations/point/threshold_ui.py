from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QHBoxLayout, QRadioButton
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI


class ThresholdUI(OperationUI):
    """Build UI for :class:`threshold.Threshold`."""

    def init_ui(self, threshold):
        """
        Create user interface for :class:`threshold.Threshold`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param threshold: The dialog threshold window
        :type threshold: :class:`threshold.Threshold`
        """

        self.operation_ui(self)
        threshold.setObjectName("threshold")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/threshold.png"), QIcon.Normal, QIcon.Off)
        threshold.setWindowIcon(icon)

        self.label_thresh_value = QLabel(threshold)
        self.label_thresh_value.setObjectName("label_thresh_value")
        self.label_thresh_value.setAlignment(Qt.AlignCenter)

        self.layout_rbtns = QHBoxLayout()
        self.layout_rbtns.setObjectName("layout_rbtns")

        self.rbtn_thresh_binary = QRadioButton("Threshold Binary")
        self.rbtn_thresh_binary.setObjectName("rbtn_thresh_binary")
        self.rbtn_thresh_binary.setLayoutDirection(Qt.RightToLeft)
        self.rbtn_thresh_binary.setChecked(True)

        self.rbtn_thresh_zero = QRadioButton("Threshold Zero")
        self.rbtn_thresh_zero.setObjectName("rbtn_thresh_zero")

        self.layout_rbtns.addWidget(self.rbtn_thresh_binary)
        self.layout_rbtns.addWidget(self.rbtn_thresh_zero)

        self.rbtn_group = QWidget(threshold)
        self.rbtn_group.setLayout(self.layout_rbtns)

        self.threshold_slider = QSlider(threshold)
        self.threshold_slider.setOrientation(Qt.Horizontal)
        self.threshold_slider.setPageStep(0)
        self.threshold_slider.setObjectName("threshold_slider")

        self.layout.addWidget(self.label_thresh_value)
        self.layout.addWidget(self.rbtn_group)
        self.layout.addWidget(self.threshold_slider)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        threshold.setLayout(self.layout)
        QMetaObject.connectSlotsByName(threshold)
