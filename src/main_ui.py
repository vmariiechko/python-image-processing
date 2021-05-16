from PyQt5.QtWidgets import QMdiArea, QMenuBar, QMenu, QAction, QActionGroup
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap

from src.constants import IMAGE_TYPES


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
        icon.addPixmap(QPixmap("icons/icon.png"), QIcon.Normal, QIcon.Off)
        main_window.setWindowIcon(icon)

        self.central_mdi_area = QMdiArea()
        self.central_mdi_area.setObjectName("mdi_area")

        main_window.setCentralWidget(self.central_mdi_area)

        self.menu_bar = QMenuBar(main_window)
        self.menu_bar.setGeometry(QRect(0, 0, 720, 21))
        self.menu_bar.setObjectName("menu_bar")

        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")

        self.menu_image = QMenu(self.menu_bar)
        self.menu_image.setObjectName("menu_image")

        self.menu_analyze = QMenu(self.menu_bar)
        self.menu_analyze.setObjectName("menu_analyze")

        self.menu_process = QMenu(self.menu_bar)
        self.menu_process.setObjectName("menu_process")

        self.menu_type = QMenu(self.menu_bar)
        self.menu_type.setObjectName("menu_type")

        self.menu_histogram = QMenu(self.menu_bar)
        self.menu_histogram.setObjectName("menu_histogram")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/histogram.png"), QIcon.Normal, QIcon.Off)
        self.menu_histogram.setIcon(icon)

        self.menu_point_operations = QMenu(self.menu_bar)
        self.menu_point_operations.setObjectName("menu_point_operations")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/point.png"), QIcon.Normal, QIcon.Off)
        self.menu_point_operations.setIcon(icon)

        self.menu_local_operations = QMenu(self.menu_bar)
        self.menu_local_operations.setObjectName("menu_local_operations")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/local.png"), QIcon.Normal, QIcon.Off)
        self.menu_local_operations.setIcon(icon)

        self.menu_segmentation = QMenu(self.menu_bar)
        self.menu_segmentation.setObjectName("menu_segmentation")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/threshold.png"), QIcon.Normal, QIcon.Off)
        self.menu_segmentation.setIcon(icon)

        self.menu_edge_detection = QMenu(main_window)
        self.menu_edge_detection.setObjectName("menu_edge_detection")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/edge.png"), QIcon.Normal, QIcon.Off)
        self.menu_edge_detection.setIcon(icon)

        main_window.setMenuBar(self.menu_bar)

        self.action_open = QAction(main_window)
        self.action_open.setObjectName("action_open")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/open.png"), QIcon.Normal, QIcon.Off)
        self.action_open.setIcon(icon)

        self.action_save = QAction(main_window)
        self.action_save.setObjectName("action_save")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/save.png"), QIcon.Normal, QIcon.Off)
        self.action_save.setIcon(icon)

        self.action_cascade = QAction(main_window)
        self.action_cascade.setObjectName("action_cascade")

        self.action_exit = QAction(main_window)
        self.action_exit.setObjectName("action_exit")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/exit.png"), QIcon.Normal, QIcon.Off)
        self.action_exit.setIcon(icon)

        self.action_rename = QAction(main_window)
        self.action_rename.setObjectName("action_rename")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/rename.png"), QIcon.Normal, QIcon.Off)
        self.action_rename.setIcon(icon)

        self.action_duplicate = QAction(main_window)
        self.action_duplicate.setObjectName("action_duplicate")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/duplicate.png"), QIcon.Normal, QIcon.Off)
        self.action_duplicate.setIcon(icon)

        self.action_histogram = QAction(main_window)
        self.action_histogram.setObjectName("action_histogram")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/histogram.png"), QIcon.Normal, QIcon.Off)
        self.action_histogram.setIcon(icon)

        self.action_profile = QAction(main_window)
        self.action_profile.setObjectName("action_profile")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/profile.png"), QIcon.Normal, QIcon.Off)
        self.action_profile.setIcon(icon)

        self.action_normalize = QAction(main_window)
        self.action_normalize.setObjectName("action_normalize")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/normalize.png"), QIcon.Normal, QIcon.Off)
        self.action_normalize.setIcon(icon)

        self.action_equalize = QAction(main_window)
        self.action_equalize.setObjectName("action_equalize")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/normalize.png"), QIcon.Normal, QIcon.Off)
        self.action_equalize.setIcon(icon)

        self.action_negation = QAction(main_window)
        self.action_negation.setObjectName("action_negation")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/negation.png"), QIcon.Normal, QIcon.Off)
        self.action_negation.setIcon(icon)

        self.action_posterize = QAction(main_window)
        self.action_posterize.setObjectName("action_posterize")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/posterize.png"), QIcon.Normal, QIcon.Off)
        self.action_posterize.setIcon(icon)

        self.action_image_calculator = QAction(main_window)
        self.action_image_calculator.setObjectName("action_image_calculator")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/image_calculator.png"), QIcon.Normal, QIcon.Off)
        self.action_image_calculator.setIcon(icon)

        self.action_smooth = QAction(main_window)
        self.action_smooth.setObjectName("action_smooth")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/smooth.png"), QIcon.Normal, QIcon.Off)
        self.action_smooth.setIcon(icon)

        self.action_edge_dt_dir = QAction(main_window)
        self.action_edge_dt_dir.setObjectName("action_edge_dt_dir")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/directions.png"), QIcon.Normal, QIcon.Off)
        self.action_edge_dt_dir.setIcon(icon)

        self.action_edge_dt_nondir = QAction(main_window)
        self.action_edge_dt_nondir.setObjectName("action_edge_dt_nondir")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/nondirectional.png"), QIcon.Normal, QIcon.Off)
        self.action_edge_dt_nondir.setIcon(icon)

        self.action_sharpen = QAction(main_window)
        self.action_sharpen.setObjectName("action_sharpen")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/sharpener.png"), QIcon.Normal, QIcon.Off)
        self.action_sharpen.setIcon(icon)

        self.action_convolve = QAction(main_window)
        self.action_convolve.setObjectName("action_convolve")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/matrix.png"), QIcon.Normal, QIcon.Off)
        self.action_convolve.setIcon(icon)

        self.action_gray_morphology = QAction(main_window)
        self.action_gray_morphology.setObjectName("action_gray_morphology")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/padlocks.png"), QIcon.Normal, QIcon.Off)
        self.action_gray_morphology.setIcon(icon)

        self.action_threshold = QAction(main_window)
        self.action_threshold.setObjectName("action_threshold")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/threshold.png"), QIcon.Normal, QIcon.Off)
        self.action_threshold.setIcon(icon)

        self.action_watershed = QAction(main_window)
        self.action_watershed.setObjectName("action_watershed")

        self.group_image_type = QActionGroup(self.menu_type)
        self.group_image_type.setObjectName("group_image_type")

        for img_type in IMAGE_TYPES:
            action = QAction(img_type, self.menu_type, checkable=True)
            self.menu_type.addAction(action)
            self.group_image_type.addAction(action)

        self.group_image_type.setExclusive(True)

        self.menu_type.addSeparator()
        self.action_color_depth_uint8 = QAction("8 bit per pixel", self.menu_type, checkable=True)
        self.menu_type.addAction(self.action_color_depth_uint8)

        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_cascade)
        self.menu_file.addAction(self.action_exit)

        self.menu_image.addAction(self.menu_type.menuAction())

        self.menu_image.addAction(self.action_rename)
        self.menu_image.addAction(self.action_duplicate)
        self.menu_analyze.addAction(self.action_histogram)
        self.menu_analyze.addAction(self.action_profile)
        self.menu_histogram.addAction(self.action_normalize)
        self.menu_histogram.addAction(self.action_equalize)
        self.menu_point_operations.addAction(self.action_negation)
        self.menu_point_operations.addAction(self.action_posterize)
        self.menu_point_operations.addAction(self.action_image_calculator)
        self.menu_edge_detection.addAction(self.action_edge_dt_dir)
        self.menu_edge_detection.addAction(self.action_edge_dt_nondir)
        self.menu_local_operations.addAction(self.action_smooth)
        self.menu_local_operations.addAction(self.action_sharpen)
        self.menu_local_operations.addAction(self.action_convolve)
        self.menu_local_operations.addAction(self.action_gray_morphology)
        self.menu_segmentation.addAction(self.action_threshold)
        self.menu_segmentation.addAction(self.action_watershed)

        self.menu_local_operations.addAction(self.menu_edge_detection.menuAction())
        self.menu_process.addAction(self.menu_histogram.menuAction())
        self.menu_process.addAction(self.menu_point_operations.menuAction())
        self.menu_process.addAction(self.menu_local_operations.menuAction())
        self.menu_process.addAction(self.menu_segmentation.menuAction())
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_image.menuAction())
        self.menu_bar.addAction(self.menu_analyze.menuAction())
        self.menu_bar.addAction(self.menu_process.menuAction())

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
        self.menu_image.setTitle(_translate(_window_title, "Image"))
        self.menu_analyze.setTitle(_translate(_window_title, "Analyze"))
        self.menu_process.setTitle(_translate(_window_title, "Process"))
        self.menu_type.setTitle(_translate(_window_title, "Type"))
        self.menu_histogram.setTitle(_translate(_window_title, "Histogram"))
        self.menu_point_operations.setTitle(_translate(_window_title, "Point Operations"))
        self.menu_local_operations.setTitle(_translate(_window_title, "Local Operations"))
        self.menu_segmentation.setTitle(_translate(_window_title, "Segmentation"))
        self.menu_edge_detection.setTitle(_translate(_window_title, "Edge Detection"))

        self.action_open.setText(_translate(_window_title, "Open"))
        self.action_save.setText(_translate(_window_title, "Save"))
        self.action_cascade.setText(_translate(_window_title, "Cascade"))
        self.action_exit.setText(_translate(_window_title, "Exit"))
        self.action_rename.setText(_translate(_window_title, "Rename"))
        self.action_duplicate.setText(_translate(_window_title, "Duplicate"))
        self.action_histogram.setText(_translate(_window_title, "Histogram"))
        self.action_profile.setText(_translate(_window_title, "Plot Profile"))
        self.action_normalize.setText(_translate(_window_title, "Normalization"))
        self.action_equalize.setText(_translate(_window_title, "Equalization"))
        self.action_negation.setText(_translate(_window_title, "Negation"))
        self.action_posterize.setText(_translate(_window_title, "Posterize"))
        self.action_image_calculator.setText(_translate(_window_title, "Image Calculator"))
        self.action_smooth.setText(_translate(_window_title, "Smooth"))
        self.action_edge_dt_dir.setText(_translate(_window_title, "Directional"))
        self.action_edge_dt_nondir.setText(_translate(_window_title, "Non-directional"))
        self.action_sharpen.setText(_translate(_window_title, "Sharpen"))
        self.action_convolve.setText(_translate(_window_title, "Convolve"))
        self.action_gray_morphology.setText(_translate(_window_title, "Gray Morphology"))
        self.action_threshold.setText(_translate(_window_title, "Threshold"))
        self.action_watershed.setText(_translate(_window_title, "Watershed"))
