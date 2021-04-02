from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt, QMetaObject


class ThresholdUI:

    def init_ui(self, threshold):
        threshold.setObjectName("threshold")

        self.label_thresh_value = QLabel(threshold)
        self.label_thresh_value.setObjectName("label_thresh_value")
        self.label_thresh_value.setAlignment(Qt.AlignCenter)

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
        self.layout.addWidget(self.threshold_slider)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        threshold.setLayout(self.layout)
        QMetaObject.connectSlotsByName(threshold)
