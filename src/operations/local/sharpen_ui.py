from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDialogButtonBox,
                             QRadioButton, QComboBox, QFormLayout)
from PyQt5.QtCore import Qt, QMetaObject, QSize
from PyQt5.QtGui import QIcon, QPixmap


class SharpenUI:
    """Build UI for :class:`sharpen.Sharpen`."""

    def init_ui(self, sharpen):
        """
        Create user interface for :class:`sharpen.Sharpen`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param sharpen: The dialog sharpen window
        :type sharpen: :class:`sharpen.Sharpen`
        """

        sharpen.setObjectName("sharpen")

        self.layout_form = QFormLayout(sharpen)
        self.layout_form.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout_form.setFormAlignment(Qt.AlignCenter)
        self.layout_form.setObjectName("layout_form")

        self.label_border_type = QLabel(sharpen)
        self.label_border_type.setObjectName("label_border_type")

        self.cb_border_type = QComboBox(sharpen)
        self.cb_border_type.addItems(["Isolated", "Reflect", "Replicate"])
        self.cb_border_type.setObjectName("cb_border_type")

        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.form = QWidget(sharpen)
        self.form.setLayout(self.layout_form)

        self.layout_masks = QHBoxLayout(sharpen)
        self.layout_masks.setObjectName("layout_masks")

        self.label_masks = QLabel()
        self.label_masks.setAlignment(Qt.AlignCenter)
        self.label_masks.setObjectName("label_masks")

        self.rbtn_mask1 = QRadioButton(sharpen)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/masks/sharpen1.png"), QIcon.Normal, QIcon.Off)
        self.rbtn_mask1.setIcon(icon)
        self.rbtn_mask1.setIconSize(QSize(123, 85))
        self.rbtn_mask1.setChecked(True)
        self.rbtn_mask1.setObjectName("rbtn_mask1")

        self.rbtn_mask2 = QRadioButton(sharpen)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/masks/sharpen2.png"), QIcon.Normal, QIcon.Off)
        self.rbtn_mask2.setIcon(icon)
        self.rbtn_mask2.setIconSize(QSize(123, 85))
        self.rbtn_mask2.setObjectName("rbtn_mask2")

        self.rbtn_mask3 = QRadioButton(sharpen)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/masks/sharpen3.png"), QIcon.Normal, QIcon.Off)
        self.rbtn_mask3.setIcon(icon)
        self.rbtn_mask3.setIconSize(QSize(123, 85))
        self.rbtn_mask3.setObjectName("rbtn_mask3")

        self.layout_masks.addWidget(self.rbtn_mask1)
        self.layout_masks.addWidget(self.rbtn_mask2)
        self.layout_masks.addWidget(self.rbtn_mask3)

        self.masks = QWidget(sharpen)
        self.masks.setLayout(self.layout_masks)

        self.label_image = QLabel(sharpen)
        self.label_image.setObjectName("label_image")
        self.label_image.setAlignment(Qt.AlignCenter)

        self.button_box = QDialogButtonBox(sharpen)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(sharpen.reject)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(sharpen.accept_changes)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_masks)
        self.layout.addWidget(self.masks)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        sharpen.setLayout(self.layout)
        sharpen.setWindowFlags(sharpen.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        QMetaObject.connectSlotsByName(sharpen)
