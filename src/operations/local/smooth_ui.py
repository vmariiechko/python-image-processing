from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QComboBox, QFormLayout
from PyQt5.QtCore import Qt, QMetaObject

from ..operation_ui import OperationUI


class SmoothUI(OperationUI):
    """Build UI for :class:`smooth.SmoothUI`."""

    def init_ui(self, smooth):
        """
        Create user interface for :class:`smooth.SmoothUI`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param smooth: The dialog smooth window
        :type smooth: :class:`smooth.SmoothUI`
        """

        self.operation_ui(self)
        smooth.setObjectName("smooth")

        self.layout_form = QFormLayout(smooth)
        self.layout_form.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout_form.setFormAlignment(Qt.AlignCenter)
        self.layout_form.setObjectName("layout_form")

        self.label_smooth_type = QLabel(smooth)
        self.label_smooth_type.setObjectName("label_kernel_size")

        self.cb_smooth_type = QComboBox(smooth)
        self.cb_smooth_type.addItems(["Blur", "Gaussian Blur"])
        self.cb_smooth_type.setObjectName("cb_border_type")

        self.label_kernel_size = QLabel(smooth)
        self.label_kernel_size.setObjectName("label_kernel_size")

        self.sb_kernel_size = QSpinBox(smooth)
        self.sb_kernel_size.setMinimum(3)
        self.sb_kernel_size.setMaximum(99)
        self.sb_kernel_size.setSingleStep(2)
        self.sb_kernel_size.setObjectName("sb_kernel_size")

        self.label_border_type = QLabel(smooth)
        self.label_border_type.setObjectName("label_border_type")

        self.cb_border_type = QComboBox(smooth)
        self.cb_border_type.addItems(["Isolated", "Reflect", "Replicate"])
        self.cb_border_type.setObjectName("cb_border_type")

        self.layout_form.addRow(self.label_smooth_type, self.cb_smooth_type)
        self.layout_form.addRow(self.label_kernel_size, self.sb_kernel_size)
        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.form = QWidget(smooth)
        self.form.setLayout(self.layout_form)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        smooth.setLayout(self.layout)
        QMetaObject.connectSlotsByName(smooth)
