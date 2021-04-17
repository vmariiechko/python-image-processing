from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt


class OperationUI:
    """The OperationUI class represents the base UI for operation UI classes."""

    def operation_ui(self, child_ui):
        """
        Create a base user interface for operation UI classes.

        The method creates main widget objects in the proper containers
        and assigns the object names to them.

        :param child_ui: The operation UI class
        """

        self.label_image = QLabel(child_ui)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setObjectName("label_image")

        self.button_box = QDialogButtonBox(child_ui)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(child_ui.reject)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(child_ui.accept_changes)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        child_ui.setWindowFlags(child_ui.windowFlags() & ~Qt.WindowContextHelpButtonHint)
