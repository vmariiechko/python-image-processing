from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QRadioButton, QFormLayout
from PyQt5.QtCore import Qt, QMetaObject

from ..operation_ui import OperationUI


class ImageCalculatorUI(OperationUI):
    """Build UI for :class:`img_calculator.ImageCalculator`."""

    def init_ui(self, img_calculator):
        """
        Create user interface for :class:`img_calculator.ImageCalculator`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param img_calculator: The image calculator dialog
        :type img_calculator: :class:`img_calculator.ImageCalculator`
        """

        self.operation_ui(self)
        img_calculator.setObjectName("img_calculator")

        self.layout_form = QFormLayout(img_calculator)
        self.layout_form.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout_form.setFormAlignment(Qt.AlignCenter)
        self.layout_form.setObjectName("layout_form")

        self.label_image1 = QLabel(img_calculator)
        self.label_image1.setObjectName("label_image1")

        self.cb_image1 = QComboBox(img_calculator)
        self.cb_image1.setObjectName("cb_image1")

        self.label_operation = QLabel(img_calculator)
        self.label_operation.setObjectName("label_operation")

        self.cb_operation = QComboBox(img_calculator)
        self.cb_operation.addItems(["Add", "Subtract", "AND", "OR", "XOR"])
        self.cb_operation.setObjectName("cb_operation")

        self.label_image2 = QLabel(img_calculator)
        self.label_image2.setObjectName("label_image2")

        self.cb_image2 = QComboBox(img_calculator)
        self.cb_image2.setObjectName("cb_image2")

        self.rbtn_resize1 = QRadioButton("Resize Image 1")
        self.rbtn_resize1.setAutoExclusive(False)
        self.rbtn_resize1.setObjectName("rbtn_resize1")

        self.rbtn_resize2 = QRadioButton("Resize Image 2")
        self.rbtn_resize2.setAutoExclusive(False)
        self.rbtn_resize2.setObjectName("rbtn_resize2")

        self.layout_form.addRow(self.label_image1, self.cb_image1)
        self.layout_form.addRow(None, self.rbtn_resize1)
        self.layout_form.addRow(self.label_operation, self.cb_operation)
        self.layout_form.addRow(self.label_image2, self.cb_image2)
        self.layout_form.addRow(None, self.rbtn_resize2)

        self.form = QWidget(img_calculator)
        self.form.setLayout(self.layout_form)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        img_calculator.setLayout(self.layout)
        QMetaObject.connectSlotsByName(img_calculator)
