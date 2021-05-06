from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QRadioButton, QSpinBox, QHBoxLayout
from PyQt5.QtCore import Qt, QMetaObject

from ..operation_ui import OperationUI
from .local_ui import LocalUI
from image.analyze import MplCanvas


class MorphologyUI(OperationUI, LocalUI):
    """Build UI for :class:`morphology.Morphology`."""

    def init_ui(self, morphology):
        """
        Create user interface for :class:`morphology.Morphology`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param morphology: The dialog morphology window
        :type morphology: :class:`morphology.Morphology`
        """

        self.operation_ui(self)
        self.local_ui(self)
        morphology.setObjectName("morphology")

        self.label_operation = QLabel(morphology)
        self.label_operation.setObjectName("label_operation")

        self.cb_operation = QComboBox(morphology)
        self.cb_operation.addItems(["Erode", "Dilate", "Open", "Close", "Top Hat", "Black Hat",
                                    "Skeletonize", "Edge Detection"])
        self.cb_operation.setObjectName("cb_operation")

        self.label_struct_element_shape = QLabel(morphology)
        self.label_struct_element_shape.setObjectName("label_struct_element_shape")

        self.cb_struct_element_shape = QComboBox(morphology)
        self.cb_struct_element_shape.addItems(["Diamond", "Rectangle", "Ellipse", "Cross"])
        self.cb_struct_element_shape.setObjectName("cb_struct_element_shape")

        self.label_iterations = QLabel(morphology)
        self.label_iterations.setObjectName("label_iterations")

        self.sb_iterations = QSpinBox(morphology)
        self.sb_iterations.setMinimum(1)
        self.sb_iterations.setMaximum(10)
        self.sb_iterations.setObjectName("sb_iterations")

        self.layout_form.addRow(self.label_operation, self.cb_operation)
        self.layout_form.addRow(self.label_struct_element_shape, self.cb_struct_element_shape)
        self.layout_form.addRow(self.label_kernel_size, self.sb_kernel_size)
        self.layout_form.addRow(self.label_iterations, self.sb_iterations)
        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        morphology.setLayout(self.layout)
        QMetaObject.connectSlotsByName(morphology)
