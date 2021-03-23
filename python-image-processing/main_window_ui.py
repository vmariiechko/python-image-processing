from PyQt5 import QtCore, QtWidgets


class MainWindowUI:
    def init_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1280, 720)

        self.central_mdi_area = QtWidgets.QMdiArea()
        self.central_mdi_area.setObjectName("mdi_area")

        main_window.setCentralWidget(self.central_mdi_area)

        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 720, 21))
        self.menu_bar.setObjectName("menu_bar")

        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")

        self.menu_analyze = QtWidgets.QMenu(self.menu_bar)
        self.menu_analyze.setObjectName("menu_analyze")

        main_window.setMenuBar(self.menu_bar)

        self.action_open = QtWidgets.QAction(main_window)
        self.action_open.setObjectName("action_open")

        self.action_histogram = QtWidgets.QAction(main_window)
        self.action_histogram.setObjectName("action_histogram")

        self.action_profile = QtWidgets.QAction(main_window)
        self.action_profile.setObjectName("action_profile")

        self.menu_file.addAction(self.action_open)
        self.menu_analyze.addAction(self.action_histogram)
        self.menu_analyze.addAction(self.action_profile)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_analyze.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate

        main_window.setWindowTitle(_translate("main_window", "APO Image Processing"))
        self.menu_file.setTitle(_translate("main_window", "File"))
        self.menu_analyze.setTitle(_translate("main_window", "Analyze"))
        self.action_open.setText(_translate("main_window", "Open"))
        self.action_histogram.setText(_translate("main_window", "Histogram"))
        self.action_profile.setText(_translate("main_window", "Plot Profile"))
