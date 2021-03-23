from PyQt5.QtCore import QMetaObject
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from hist_window_ui import MplCanvas


class IntensityProfileUI:
    def init_ui(self, profile):

        self.profile_plot = MplCanvas(profile)
        self.profile_plot.setObjectName("profile_plot")

        self.toolbar = NavigationToolbar(self.profile_plot, self)
        self.toolbar.setObjectName("toolbar")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.profile_plot)

        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.widget.setLayout(self.layout)

        profile.setWidget(self.widget)
        QMetaObject.connectSlotsByName(profile)
