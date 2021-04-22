from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QSpinBox, QDoubleSpinBox,
                             QRadioButton, QHBoxLayout, QVBoxLayout, QFormLayout)
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

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

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/image_calculator.png"), QIcon.Normal, QIcon.Off)
        img_calculator.setWindowIcon(icon)

        # =========== First image form ===========
        self.label_image1 = QLabel(img_calculator)
        self.label_image1.setObjectName("label_image1")

        self.cb_image1 = QComboBox(img_calculator)
        self.cb_image1.setObjectName("cb_image1")

        self.label_weight1 = QLabel(img_calculator)
        self.label_weight1.setObjectName("label_weight1")

        self.sb_weight1 = QDoubleSpinBox(img_calculator)
        self.sb_weight1.setDecimals(1)
        self.sb_weight1.setMinimum(0.1)
        self.sb_weight1.setMaximum(1.0)
        self.sb_weight1.setSingleStep(0.1)
        self.sb_weight1.setEnabled(False)
        self.sb_weight1.setObjectName("sb_weight1")

        self.rbtn_resize1 = QRadioButton("Resize Image 1")
        self.rbtn_resize1.setAutoExclusive(False)
        self.rbtn_resize1.setObjectName("rbtn_resize1")
        
        layout_form1 = QFormLayout()
        layout_form1.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        layout_form1.setFormAlignment(Qt.AlignCenter)

        layout_form1.addRow(self.label_image1, self.cb_image1)
        layout_form1.addRow(self.label_weight1, self.sb_weight1)
        layout_form1.addRow(None, self.rbtn_resize1)

        self.form1 = QWidget()
        self.form1.setLayout(layout_form1)

        # =========== Operation and Gamma middle form ===========
        self.label_operation = QLabel(img_calculator)
        self.label_operation.setAlignment(Qt.AlignCenter)
        self.label_operation.setObjectName("label_operation")

        self.cb_operation = QComboBox(img_calculator)
        self.cb_operation.addItems(["Add", "Subtract", "Blend", "AND", "OR", "XOR"])
        self.cb_operation.setObjectName("cb_operation")

        self.label_gamma = QLabel(img_calculator)
        self.label_gamma.setAlignment(Qt.AlignCenter)
        self.label_gamma.setObjectName("label_gamma")

        self.sb_gamma = QSpinBox(img_calculator)
        self.sb_gamma.setEnabled(False)
        self.sb_gamma.setObjectName("sb_gamma")

        layout_form_mid = QVBoxLayout()

        layout_form_mid.addWidget(self.label_operation)
        layout_form_mid.addWidget(self.cb_operation)
        layout_form_mid.addWidget(self.label_gamma)
        layout_form_mid.addWidget(self.sb_gamma)

        self.form_mid = QWidget()
        self.form_mid.setLayout(layout_form_mid)

        # =========== Second image form ===========
        self.label_image2 = QLabel(img_calculator)
        self.label_image2.setObjectName("label_image2")

        self.cb_image2 = QComboBox(img_calculator)
        self.cb_image2.setObjectName("cb_image2")

        self.label_weight2 = QLabel(img_calculator)
        self.label_weight2.setObjectName("label_weight2")

        self.sb_weight2 = QDoubleSpinBox(img_calculator)
        self.sb_weight2.setDecimals(1)
        self.sb_weight2.setMinimum(0)
        self.sb_weight2.setMaximum(1.0)
        self.sb_weight2.setSingleStep(0.1)
        self.sb_weight2.setEnabled(False)
        self.sb_weight2.setObjectName("sb_weight2")

        self.rbtn_resize2 = QRadioButton("Resize Image 2")
        self.rbtn_resize2.setAutoExclusive(False)
        self.rbtn_resize2.setObjectName("rbtn_resize2")

        layout_form2 = QFormLayout()
        layout_form2.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        layout_form2.setFormAlignment(Qt.AlignCenter)

        layout_form2.addRow(self.label_image2, self.cb_image2)
        layout_form2.addRow(self.label_weight2, self.sb_weight2)
        layout_form2.addRow(None, self.rbtn_resize2)

        self.form2 = QWidget()
        self.form2.setLayout(layout_form2)

        # =========== Main form ===========
        self.form_layout = QHBoxLayout(img_calculator)
        self.form_layout.setObjectName("form_layout")

        self.form_layout.addWidget(self.form1)
        self.form_layout.addWidget(self.form_mid)
        self.form_layout.addWidget(self.form2)

        self.form = QWidget(img_calculator)
        self.form.setLayout(self.form_layout)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        img_calculator.setLayout(self.layout)
        QMetaObject.connectSlotsByName(img_calculator)
