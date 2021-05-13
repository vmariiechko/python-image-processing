from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QComboBox, QFormLayout
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from .operation_ui import OperationUI


class SegmentationUI(OperationUI):
    """Build UI for :class:`segmentation.Segmentation`."""

    def init_ui(self, segmentation):
        """
        Create user interface for :class:`segmentation.Segmentation`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param segmentation: The dialog segmentation window
        :type segmentation: :class:`segmentation.Segmentation`
        """

        self.operation_ui(self)
        segmentation.setObjectName("segmentation")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/threshold.png"), QIcon.Normal, QIcon.Off)
        segmentation.setWindowIcon(icon)

        self.layout_form = QFormLayout(segmentation)
        self.layout_form.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout_form.setFormAlignment(Qt.AlignCenter)
        self.layout_form.setObjectName("layout_form")

        self.label_thresh_txt = QLabel(segmentation)
        self.label_thresh_txt.setObjectName("label_thresh_txt")
        self.label_thresh_txt.setAlignment(Qt.AlignCenter)

        self.label_thresh_value = QLabel(segmentation)
        self.label_thresh_value.setObjectName("label_thresh_value")
        self.label_thresh_value.setAlignment(Qt.AlignCenter)

        self.label_segmentation_type = QLabel(segmentation)
        self.label_segmentation_type.setObjectName("label_segmentation_type")

        self.cb_segmentation_type = QComboBox(segmentation)
        self.cb_segmentation_type.addItems(["Threshold Binary", "Threshold Zero"])
        self.cb_segmentation_type.setObjectName("cb_segmentation_type")

        self.layout_form.addRow(self.label_thresh_txt, self.label_thresh_value)
        self.layout_form.addRow(self.label_segmentation_type, self.cb_segmentation_type)

        self.form = QWidget(segmentation)
        self.form.setLayout(self.layout_form)

        self.threshold_slider = QSlider(segmentation)
        self.threshold_slider.setOrientation(Qt.Horizontal)
        self.threshold_slider.setPageStep(0)
        self.threshold_slider.setObjectName("threshold_slider")

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.threshold_slider)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        segmentation.setLayout(self.layout)
        QMetaObject.connectSlotsByName(segmentation)
