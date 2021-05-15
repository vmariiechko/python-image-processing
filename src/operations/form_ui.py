from PyQt5.QtWidgets import QWidget, QFormLayout
from PyQt5.QtCore import Qt


class FormUI:
    """The FormUI class implements the base form for operation UI classes."""

    def form_ui(self, child_ui):
        """
        Create a base form for operation UI classes.

        The method creates main widget objects in the proper containers
        and assigns the object names to them.

        :param child_ui: The operation UI class
        """

        self.layout_form = QFormLayout(child_ui)
        self.layout_form.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout_form.setFormAlignment(Qt.AlignCenter)
        self.layout_form.setObjectName("layout_form")

        self.form = QWidget(child_ui)
        self.form.setLayout(self.layout_form)
        self.form.setObjectName("form")
