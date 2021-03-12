from PyQt5 import QtCore, QtWidgets


class MainWindowUI:
    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(475, 70)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 475, 21))
        self.menu_bar.setObjectName("menu_bar")

        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")

        main_window.setMenuBar(self.menu_bar)

        self.action_open = QtWidgets.QAction(main_window)
        self.action_open.setObjectName("action_open")

        self.menu_file.addAction(self.action_open)
        self.menu_bar.addAction(self.menu_file.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate

        main_window.setWindowTitle(_translate("main_window", "main_window"))
        self.menu_file.setTitle(_translate("main_window", "File"))
        self.action_open.setText(_translate("main_window", "Open"))
