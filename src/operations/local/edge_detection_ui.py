from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QComboBox, QFormLayout
from PyQt5.QtCore import Qt, QMetaObject

from ..operation_ui import OperationUI


class EdgeDetectionUI(OperationUI):
    """Build UI for :class:`edge_detection.EdgeDetection`."""

    def init_ui(self, edge_dt):
        """
        Create user interface for :class:`edge_detection.EdgeDetection`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param edge_dt: The dialog edge detection window
        :type edge_dt: :class:`edge_detection.EdgeDetection`
        """

        self.operation_ui(self)
        edge_dt.setObjectName("edge_dt")

        self.layout_form = QFormLayout(edge_dt)
        self.layout_form.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout_form.setFormAlignment(Qt.AlignCenter)
        self.layout_form.setObjectName("layout_form")

        self.label_edge_dt_type = QLabel(edge_dt)
        self.label_edge_dt_type.setObjectName("label_kernel_size")

        self.cb_edge_dt_type = QComboBox(edge_dt)
        self.cb_edge_dt_type.addItems(["Sobel", "Laplacian", "Canny"])
        self.cb_edge_dt_type.setObjectName("cb_border_type")

        self.label_kernel_size = QLabel(edge_dt)
        self.label_kernel_size.setObjectName("label_kernel_size")

        self.sb_kernel_size = QSpinBox(edge_dt)
        self.sb_kernel_size.setMinimum(3)
        self.sb_kernel_size.setMaximum(31)
        self.sb_kernel_size.setSingleStep(2)
        self.sb_kernel_size.setObjectName("sb_kernel_size")

        self.label_border_type = QLabel(edge_dt)
        self.label_border_type.setObjectName("label_border_type")

        self.cb_border_type = QComboBox(edge_dt)
        self.cb_border_type.addItems(["Isolated", "Reflect", "Replicate"])
        self.cb_border_type.setObjectName("cb_border_type")

        self.label_low_threshold = QLabel(edge_dt)
        self.label_low_threshold.setObjectName("label_low_threshold")

        self.sb_low_threshold = QSpinBox(edge_dt)
        self.sb_low_threshold.setMinimum(1)
        self.sb_low_threshold.setObjectName("sb_low_threshold")

        self.label_high_threshold = QLabel(edge_dt)
        self.label_high_threshold.setObjectName("label_high_threshold")

        self.sb_high_threshold = QSpinBox(edge_dt)
        self.sb_high_threshold.setMinimum(2)
        self.sb_high_threshold.setObjectName("sb_high_threshold")

        self.layout_form.addRow(self.label_edge_dt_type, self.cb_edge_dt_type)
        self.layout_form.addRow(self.label_kernel_size, self.sb_kernel_size)
        self.layout_form.addRow(self.label_border_type, self.cb_border_type)
        self.layout_form.addRow(self.label_low_threshold, self.sb_low_threshold)
        self.layout_form.addRow(self.label_high_threshold, self.sb_high_threshold)

        self.form = QWidget(edge_dt)
        self.form.setLayout(self.layout_form)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        edge_dt.setLayout(self.layout)
        QMetaObject.connectSlotsByName(edge_dt)
