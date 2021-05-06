from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QRadioButton, QSizePolicy
from PyQt5.QtCore import Qt, QSize, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI
from .local_ui import LocalUI


class SharpenUI(OperationUI, LocalUI):
    """Build UI for :class:`sharpen.Sharpen`."""

    def init_ui(self, sharpen):
        """
        Create user interface for :class:`sharpen.Sharpen`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param sharpen: The dialog sharpen window
        :type sharpen: :class:`sharpen.Sharpen`
        """

        self.operation_ui(self)
        self.local_ui(self)
        sharpen.setObjectName("sharpen")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/sharpener.png"), QIcon.Normal, QIcon.Off)
        sharpen.setWindowIcon(icon)

        self.label_kernel_size.setVisible(False)
        self.sb_kernel_size.setVisible(False)

        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.layout_masks = QHBoxLayout(sharpen)
        self.layout_masks.setObjectName("layout_masks")

        self.label_masks = QLabel()
        self.label_masks.setAlignment(Qt.AlignCenter)
        self.label_masks.setObjectName("label_masks")

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.rbtn_mask1 = QRadioButton(sharpen)
        self.rbtn_mask1.setSizePolicy(size_policy)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/masks/sharpen1.png"), QIcon.Normal, QIcon.Off)
        self.rbtn_mask1.setIcon(icon)
        self.rbtn_mask1.setIconSize(QSize(135, 100))
        self.rbtn_mask1.setChecked(True)
        self.rbtn_mask1.setObjectName("rbtn_mask1")

        self.rbtn_mask2 = QRadioButton(sharpen)
        self.rbtn_mask2.setSizePolicy(size_policy)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/masks/sharpen2.png"), QIcon.Normal, QIcon.Off)
        self.rbtn_mask2.setIcon(icon)
        self.rbtn_mask2.setIconSize(QSize(135, 100))
        self.rbtn_mask2.setObjectName("rbtn_mask2")

        self.rbtn_mask3 = QRadioButton(sharpen)
        self.rbtn_mask3.setSizePolicy(size_policy)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/masks/sharpen3.png"), QIcon.Normal, QIcon.Off)
        self.rbtn_mask3.setIcon(icon)
        self.rbtn_mask3.setIconSize(QSize(135, 100))
        self.rbtn_mask3.setObjectName("rbtn_mask3")

        self.layout_masks.addWidget(self.rbtn_mask1)
        self.layout_masks.addWidget(self.rbtn_mask2)
        self.layout_masks.addWidget(self.rbtn_mask3)

        self.masks = QWidget(sharpen)
        self.masks.setLayout(self.layout_masks)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_masks)
        self.layout.addWidget(self.masks)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        sharpen.setLayout(self.layout)
        QMetaObject.connectSlotsByName(sharpen)
