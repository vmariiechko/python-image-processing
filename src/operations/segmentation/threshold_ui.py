from PyQt5.QtWidgets import QLabel, QSlider, QComboBox
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI
from ..form_ui import FormUI


class ThresholdUI(OperationUI, FormUI):
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
        self.form_ui(self)
        threshold.setObjectName("threshold")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/threshold.png"), QIcon.Normal, QIcon.Off)
        threshold.setWindowIcon(icon)

        self.label_slider_txt = QLabel(threshold)
        self.label_slider_txt.setObjectName("label_slider_txt")

        self.label_slider_value = QLabel(threshold)
        self.label_slider_value.setObjectName("label_slider_value")

        self.label_threshold_type = QLabel(threshold)
        self.label_threshold_type.setObjectName("label_threshold_type")

        self.cb_threshold_type = QComboBox(threshold)
        self.cb_threshold_type.addItems(["Threshold Binary", "Threshold Zero", "Adaptive Mean Threshold",
                                         "Adaptive Gaussian Threshold", "Threshold Otsu Method"])
        self.cb_threshold_type.setObjectName("cb_threshold_type")

        self.layout_form.addRow(self.label_slider_txt, self.label_slider_value)
        self.layout_form.addRow(self.label_threshold_type, self.cb_threshold_type)

        self.threshold_slider = QSlider(threshold)
        self.threshold_slider.setOrientation(Qt.Horizontal)
        self.threshold_slider.setPageStep(0)
        self.threshold_slider.setObjectName("threshold_slider")

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.threshold_slider)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        threshold.setLayout(self.layout)
        QMetaObject.connectSlotsByName(threshold)
