from PyQt5.QtWidgets import QLabel, QComboBox
from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI
from .local_ui import LocalUI


class SmoothUI(OperationUI, LocalUI):
    """Build UI for :class:`smooth.SmoothUI`."""

    def init_ui(self, smooth):
        """
        Create user interface for :class:`smooth.SmoothUI`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param smooth: The dialog smooth window
        :type smooth: :class:`smooth.SmoothUI`
        """

        self.operation_ui(self)
        self.local_ui(self)
        smooth.setObjectName("smooth")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/smooth.png"), QIcon.Normal, QIcon.Off)
        smooth.setWindowIcon(icon)

        self.label_smooth_type = QLabel(smooth)
        self.label_smooth_type.setObjectName("label_kernel_size")

        self.cb_smooth_type = QComboBox(smooth)
        self.cb_smooth_type.addItems(["Blur", "Gaussian Blur", "Median Blur"])
        self.cb_smooth_type.setObjectName("cb_border_type")

        self.layout_form.addRow(self.label_smooth_type, self.cb_smooth_type)
        self.layout_form.addRow(self.label_kernel_size, self.sb_kernel_size)
        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        smooth.setLayout(self.layout)
        QMetaObject.connectSlotsByName(smooth)
