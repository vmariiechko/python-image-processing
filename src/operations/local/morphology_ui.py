from PyQt5.QtWidgets import QLabel, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QMetaObject

from ..operation_ui import OperationUI
from .local_ui import LocalUI


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

        self.label_operator = QLabel(morphology)
        self.label_operator.setObjectName("label_operator")

        self.cb_operator = QComboBox(morphology)
        self.cb_operator.addItems(["Erode", "Dilate", "Open", "Close"])
        self.cb_operator.setObjectName("cb_operator")

        self.label_structure_element = QLabel(morphology)
        self.label_structure_element.setObjectName("label_structure_element")

        self.cb_structure_element = QComboBox(morphology)
        self.cb_structure_element.addItems(["Diamond", "Rectangle"])
        self.cb_structure_element.setObjectName("cb_structure_element")

        self.layout_form.addRow(self.label_operator, self.cb_operator)
        self.layout_form.addRow(self.label_structure_element, self.cb_structure_element)
        self.layout_form.addRow(self.label_kernel_size, self.sb_kernel_size)
        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        morphology.setLayout(self.layout)
        QMetaObject.connectSlotsByName(morphology)
