from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt


class OperationUI:
    """The OperationUI class represents the base UI for operation UI classes."""

    def operation_ui(self, base):
        """
        Create a base user interface for operation UI classes.

        The method creates main widget objects in the proper containers
        and assigns the object names to them.

        :param base: The operation UI class
        """

        self.label_image = QLabel(base)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setObjectName("label_image")

        self.button_box = QDialogButtonBox(base)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(base.reject)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(base.accept_changes)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        base.setWindowFlags(base.windowFlags() & ~Qt.WindowContextHelpButtonHint)
