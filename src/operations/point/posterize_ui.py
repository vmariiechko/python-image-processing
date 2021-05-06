from PyQt5.QtWidgets import QLabel, QSlider
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI


class PosterizeUI(OperationUI):
    """Build UI for :class:`posterize.Posterize`."""

    def init_ui(self, posterize):
        """
        Create user interface for :class:`posterize.Posterize`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param posterize: The dialog posterize window
        :type posterize: :class:`posterize.Posterize`
        """

        self.operation_ui(self)
        posterize.setObjectName("posterize")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/posterize.png"), QIcon.Normal, QIcon.Off)
        posterize.setWindowIcon(icon)

        self.label_bins_num = QLabel(posterize)
        self.label_bins_num.setObjectName("label_bins_num")
        self.label_bins_num.setAlignment(Qt.AlignCenter)

        self.bins_slider = QSlider(posterize)
        self.bins_slider.setOrientation(Qt.Horizontal)
        self.bins_slider.setObjectName("bins_slider")

        self.layout.addWidget(self.label_bins_num)
        self.layout.addWidget(self.bins_slider)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        posterize.setLayout(self.layout)
        QMetaObject.connectSlotsByName(posterize)
