from PyQt5.QtWidgets import (QLabel, QPushButton, QListWidget, QDialogButtonBox, QComboBox,
                             QGridLayout, QVBoxLayout, QSizePolicy)
from PyQt5.QtCore import Qt, QMetaObject

from src.operations.form_ui import FormUI


class ImagePanoramaUI(FormUI):
    """Build UI for :class:`panorama.ImagePanorama`."""

    def init_ui(self, panorama):
        """
        Create user interface for :class:`panorama.ImagePanorama`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param panorama: The image panorama dialog
        :type panorama: :class:`panorama.ImagePanorama`
        """

        panorama.setObjectName("panorama")
        self.form_ui(panorama)

        self.label_mode = QLabel()
        self.label_mode.setObjectName("label_mode")

        self.cb_mode = QComboBox(panorama)
        self.cb_mode.addItems(["Default", "Default Cropped", "Manual"])
        self.cb_mode.setObjectName("cb_mode")

        self.layout_form.addRow(self.label_mode, self.cb_mode)

        self.label_errors = QLabel()
        self.label_errors.setStyleSheet("color: red")
        self.label_errors.setAlignment(Qt.AlignCenter)
        self.label_errors.setObjectName("label_errors")

        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName("grid_layout")

        self.label_left_list = QLabel()
        self.label_left_list.setObjectName("label_left_list")

        self.left_list = QListWidget(panorama)
        self.left_list.setObjectName("left_list")

        self.grid_layout.addWidget(self.label_left_list, 1, 0, 1, 4, alignment=Qt.AlignCenter)
        self.grid_layout.addWidget(self.left_list, 2, 0, 4, 4)

        self.buttons = dict()
        self.buttons['>>'] = QPushButton('>>')
        self.buttons['>'] = QPushButton('>')
        self.buttons['<'] = QPushButton('<')
        self.buttons['<<'] = QPushButton('<<')

        for b in self.buttons:
            self.buttons[b].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
            self.buttons[b].setFocusPolicy(Qt.NoFocus)

        self.grid_layout.setRowStretch(5, 1)
        self.grid_layout.addWidget(self.buttons['>>'], 2, 4, 1, 1, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(self.buttons['>'], 3, 4, 1, 1, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(self.buttons['<'], 4, 4, 1, 1, alignment=Qt.AlignTop)
        self.grid_layout.addWidget(self.buttons['<<'], 5, 4, 1, 1, alignment=Qt.AlignTop)

        self.label_right_list = QLabel()
        self.label_right_list.setObjectName("label_right_list")

        self.right_list = QListWidget(panorama)
        self.right_list.setObjectName("right_list")

        self.grid_layout.addWidget(self.label_right_list, 1, 5, 1, 4, alignment=Qt.AlignCenter)
        self.grid_layout.addWidget(self.right_list, 2, 5, 4, 4)

        self.button_box = QDialogButtonBox(panorama)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(panorama.reject)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(panorama.stitch_images)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout(panorama)
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_errors)
        self.layout.addLayout(self.grid_layout)
        self.layout.addWidget(self.button_box)

        panorama.setLayout(self.layout)
        panorama.setWindowFlags(panorama.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        QMetaObject.connectSlotsByName(panorama)

    def set_widget_connections(self):
        """Connect widgets to methods."""

        self.left_list.itemSelectionChanged.connect(self.update_button_status)
        self.right_list.itemSelectionChanged.connect(self.update_button_status)

        self.buttons['>'].clicked.connect(self.button_add_clicked)
        self.buttons['<'].clicked.connect(self.button_remove_clicked)
        self.buttons['>>'].clicked.connect(self.button_add_all_clicked)
        self.buttons['<<'].clicked.connect(self.button_remove_all_clicked)

    def button_add_clicked(self):
        """Move a selected item from the left list to the right."""

        row = self.left_list.currentRow()
        row_item = self.left_list.takeItem(row)
        self.right_list.addItem(row_item)

    def button_remove_clicked(self):
        """Move a selected item from the right list to the left."""

        row = self.right_list.currentRow()
        row_item = self.right_list.takeItem(row)
        self.left_list.addItem(row_item)

    def button_add_all_clicked(self):
        """Move all items from the left list to the right."""

        for i in range(self.left_list.count()):
            self.right_list.addItem(self.left_list.takeItem(0))

    def button_remove_all_clicked(self):
        """Move all items from the right list to the left."""

        for i in range(self.right_list.count()):
            self.left_list.addItem(self.right_list.takeItem(0))

    def update_button_status(self):
        """Update buttons access whenever move items."""

        self.buttons['>'].setDisabled(not bool(self.left_list.selectedItems()) or self.left_list.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.right_list.selectedItems()) or self.right_list.count() == 0)
