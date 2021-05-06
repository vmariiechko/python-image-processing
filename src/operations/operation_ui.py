from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QRadioButton,
                             QHBoxLayout, QDialogButtonBox, QSizePolicy)
from PyQt5.QtCore import Qt

from image.analyze import MplCanvas


class OperationUI:
    """The OperationUI class represents the base UI for operation UI classes."""

    def operation_ui(self, child_ui):
        """
        Create a base user interface for operation UI classes.

        The method creates main widget objects in the proper containers
        and assigns the object names to them.

        :param child_ui: The operation UI class
        """

        self.layout_show_hist = QHBoxLayout(child_ui)
        self.layout_show_hist.setObjectName("layout_show_hist")

        self.rbtn_show_hist = QRadioButton("Show histogram")
        self.rbtn_show_hist.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.rbtn_show_hist.setObjectName("rbtn_show_hist")

        self.layout_show_hist.addWidget(self.rbtn_show_hist)

        self.show_hist_widget = QWidget(child_ui)
        self.show_hist_widget.setObjectName("show_hist_widget")
        self.show_hist_widget.setLayout(self.layout_show_hist)

        self.layout_preview = QHBoxLayout(child_ui)
        self.layout_preview.setObjectName("layout_preview")

        self.label_image = QLabel(child_ui)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setObjectName("label_image")

        self.hist_canvas = MplCanvas(child_ui, width=6)
        self.hist_canvas.setObjectName("hist_canvas")
        self.hist_canvas.setVisible(False)

        self.layout_preview.addWidget(self.label_image)
        self.layout_preview.addWidget(self.hist_canvas)

        self.preview_widget = QWidget(child_ui)
        self.preview_widget.setObjectName("preview_widget")
        self.preview_widget.setLayout(self.layout_preview)

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
