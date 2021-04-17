from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QComboBox, QFormLayout
from PyQt5.QtCore import Qt


class LocalUI:
    """The LocalUI class represents the base UI for local operation UI classes."""

    def local_ui(self, child_ui):
        """
        Create a base user interface for local operation UI classes.

        The method creates main widget objects in the proper containers
        and assigns the object names to them.

        :param child_ui: The local operation UI class
        """

        self.layout_form = QFormLayout(child_ui)
        self.layout_form.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout_form.setFormAlignment(Qt.AlignCenter)
        self.layout_form.setObjectName("layout_form")

        self.label_kernel_size = QLabel(child_ui)
        self.label_kernel_size.setObjectName("label_kernel_size")

        self.sb_kernel_size = QSpinBox(child_ui)
        self.sb_kernel_size.setMinimum(3)
        self.sb_kernel_size.setMaximum(31)
        self.sb_kernel_size.setSingleStep(2)
        self.sb_kernel_size.setObjectName("sb_kernel_size")

        self.label_border_type = QLabel(child_ui)
        self.label_border_type.setObjectName("label_border_type")

        self.cb_border_type = QComboBox(child_ui)
        self.cb_border_type.addItems(["Isolated", "Reflect", "Replicate"])
        self.cb_border_type.setObjectName("cb_border_type")

        self.form = QWidget(child_ui)
        self.form.setLayout(self.layout_form)
