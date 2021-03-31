from PyQt5.QtWidgets import QMdiArea, QMenuBar, QMenu, QAction
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap


class MainWindowUI:
    """Build UI for :class:`main_window.ManWindow`."""

    def init_ui(self, main_window):
        """
        Create user interface for :class:`main_window.ManWindow`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param main_window: The main window of program
        :type main_window: :class:`main_window.MainWindow`
        """

        main_window.setObjectName("main_window")
        main_window.resize(1280, 720)

        icon = QIcon()
        icon.addPixmap(QPixmap("images/icon.png"), QIcon.Normal, QIcon.Off)
        main_window.setWindowIcon(icon)

        self.central_mdi_area = QMdiArea()
        self.central_mdi_area.setObjectName("mdi_area")

        main_window.setCentralWidget(self.central_mdi_area)

        self.menu_bar = QMenuBar(main_window)
        self.menu_bar.setGeometry(QRect(0, 0, 720, 21))
        self.menu_bar.setObjectName("menu_bar")

        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")

        self.menu_analyze = QMenu(self.menu_bar)
        self.menu_analyze.setObjectName("menu_analyze")

        self.menu_operations = QMenu(self.menu_bar)
        self.menu_operations.setObjectName("menu_operations")

        self.menu_histogram = QMenu(self.menu_bar)
        self.menu_histogram.setObjectName("menu_histogram")

        main_window.setMenuBar(self.menu_bar)

        self.action_open = QAction(main_window)
        self.action_open.setObjectName("action_open")

        self.action_histogram = QAction(main_window)
        self.action_histogram.setObjectName("action_histogram")

        self.action_profile = QAction(main_window)
        self.action_profile.setObjectName("action_profile")

        self.action_normalize = QAction(main_window)
        self.action_normalize.setObjectName("action_normalize")

        self.action_equalize = QAction(main_window)
        self.action_equalize.setObjectName("action_equalize")

        self.menu_file.addAction(self.action_open)
        self.menu_analyze.addAction(self.action_histogram)
        self.menu_analyze.addAction(self.action_profile)
        self.menu_histogram.addAction(self.action_normalize)
        self.menu_histogram.addAction(self.action_equalize)

        self.menu_operations.addAction(self.menu_histogram.menuAction())
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_analyze.menuAction())
        self.menu_bar.addAction(self.menu_operations.menuAction())

        self.retranslate_ui(main_window)
        QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        """
        Set the text and titles of the widgets.

        :param main_window: The main window of program
        :type main_window: :class:`main_window.MainWindow`
        """

        _translate = QCoreApplication.translate
        _window_title = "main_window"

        main_window.setWindowTitle(_translate(_window_title, "APO Image Processing"))
        self.menu_file.setTitle(_translate(_window_title, "File"))
        self.menu_analyze.setTitle(_translate(_window_title, "Analyze"))
        self.menu_operations.setTitle(_translate(_window_title, "Operations"))
        self.menu_histogram.setTitle(_translate(_window_title, "Histogram"))
        self.action_open.setText(_translate(_window_title, "Open"))
        self.action_histogram.setText(_translate(_window_title, "Histogram"))
        self.action_profile.setText(_translate(_window_title, "Plot Profile"))
        self.action_normalize.setText(_translate(_window_title, "Normalization"))
        self.action_equalize.setText(_translate(_window_title, "Equalization"))
