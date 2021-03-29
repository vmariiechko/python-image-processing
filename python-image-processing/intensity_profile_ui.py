from PyQt5.QtCore import QMetaObject
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from hist_window_ui import MplCanvas


class IntensityProfileUI:
    """Build UI for :class:`intensity_profile.IntensityProfile`."""

    def init_ui(self, profile):
        """
        Create user interface for :class:`intensity_profile.IntensityProfile`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param profile: The window for graphical representation of profile
        :type profile: :class:`intensity_profile.IntensityProfile`
        """

        icon = QIcon()
        icon.addPixmap(QPixmap("images/histogram.png"), QIcon.Normal, QIcon.Off)
        profile.setWindowIcon(icon)

        self.profile_canvas = MplCanvas(profile)
        self.profile_canvas.setObjectName("profile_canvas")

        self.toolbar = NavigationToolbar(self.profile_canvas, self)
        self.toolbar.setObjectName("toolbar")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.profile_canvas)

        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.widget.setLayout(self.layout)

        profile.setWidget(self.widget)
        QMetaObject.connectSlotsByName(profile)
