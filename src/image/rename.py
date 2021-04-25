from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDialogButtonBox, QFormLayout, QWidget
from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication


class RenameUI:
    """Build UI for :class:`rename.Rename`."""

    def init_ui(self, rename):
        """
        Create user interface for :class:`rename.Rename`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param rename: The dialog rename window
        :type rename: :class:`rename.Rename`
        """

        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.form_layout.setFormAlignment(Qt.AlignCenter)

        self.label_title = QLabel()
        self.label_title.setObjectName("label_title")

        self.edit_title = QLineEdit()
        self.edit_title.setObjectName("edit_title")

        self.button_box = QDialogButtonBox(rename)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(rename.reject)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(rename.accept_changes)
        self.button_box.setObjectName("button_box")

        self.form_layout.addRow(self.label_title, self.edit_title)
        self.form_layout.addRow(QWidget())
        self.form_layout.addRow(self.button_box)

        rename.setLayout(self.form_layout)
        QMetaObject.connectSlotsByName(rename)
        rename.setWindowFlags(rename.windowFlags() & ~Qt.WindowContextHelpButtonHint)


class Rename(QDialog, RenameUI):
    """The Rename class implements an image rename dialog."""

    def __init__(self, img_name):
        """
        Create a new dialog window to rename the image.

        :param img_name: The old image name
        :type img_name: str
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.new_name = img_name
        self.edit_title.setText(img_name)

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Rename"

        self.setWindowTitle(_window_title)
        self.label_title.setText(_translate(_window_title, "Title:"))

    def accept_changes(self):
        """Accept changed image name to the original one."""

        self.new_name = self.edit_title.text().strip()
        self.accept()
