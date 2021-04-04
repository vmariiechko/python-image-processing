from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap


class PosterizeUI:
    """Build UI for :class:`posterize.Posterize`."""

    def init_ui(self, posterize):
        """
        Create user interface for :class:`posterize.Posterize`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param posterize: The dialog posterize window
        :type posterize: :class:`posterize.Posterize`
        """

        posterize.setObjectName("posterize")

        icon = QIcon()
        icon.addPixmap(QPixmap("images/posterize.png"), QIcon.Normal, QIcon.Off)
        posterize.setWindowIcon(icon)

        self.label_bins_num = QLabel(posterize)
        self.label_bins_num.setObjectName("label_bins_num")
        self.label_bins_num.setAlignment(Qt.AlignCenter)

        self.bins_slider = QSlider(posterize)
        self.bins_slider.setOrientation(Qt.Horizontal)
        self.bins_slider.setObjectName("bins_slider")

        self.label_image = QLabel(posterize)
        self.label_image.setObjectName("label_image")
        self.label_image.setAlignment(Qt.AlignCenter)

        self.button_box = QDialogButtonBox(posterize)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(posterize.reject)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.label_bins_num)
        self.layout.addWidget(self.bins_slider)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        posterize.setLayout(self.layout)
        posterize.setWindowFlags(posterize.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        QMetaObject.connectSlotsByName(posterize)
