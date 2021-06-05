from PyQt5.QtWidgets import QMdiArea, QMenuBar, QStatusBar, QToolBar, QMenu, QAction, QActionGroup
from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence

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

        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("status_bar")

        self.file__toolbar = QToolBar("File", main_window)
        self.image__toolbar = QToolBar("Image", main_window)
        self.analyze__toolbar = QToolBar("Analyze", main_window)

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
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/picture_mix.png"), QIcon.Normal, QIcon.Off)
        self.menu_type.setIcon(icon)

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
        icon.addPixmap(QPixmap("icons/segmentation.png"), QIcon.Normal, QIcon.Off)
        self.menu_segmentation.setIcon(icon)

        self.menu_edge_detection = QMenu(main_window)
        self.menu_edge_detection.setObjectName("menu_edge_detection")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/edge.png"), QIcon.Normal, QIcon.Off)
        self.menu_edge_detection.setIcon(icon)

        main_window.setMenuBar(self.menu_bar)
        main_window.setStatusBar(self.status_bar)

        main_window.addToolBar(self.file__toolbar)
        main_window.addToolBar(self.image__toolbar)
        main_window.addToolBar(Qt.LeftToolBarArea, self.analyze__toolbar)

        self.action_panorama = QAction(main_window)
        self.action_panorama.setObjectName("action_panorama")

        self.action_program_info = QAction(main_window)
        self.action_program_info.setObjectName("action_program_info")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/info.png"), QIcon.Normal, QIcon.Off)
        self.action_program_info.setIcon(icon)

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

        self.action_undo = QAction(main_window)
        self.action_undo.setEnabled(False)
        self.action_undo.setObjectName("action_undo")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/undo.png"), QIcon.Normal, QIcon.Off)
        self.action_undo.setIcon(icon)

        self.action_cascade = QAction(main_window)
        self.action_cascade.setObjectName("action_cascade")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/cascade.png"), QIcon.Normal, QIcon.Off)
        self.action_cascade.setIcon(icon)

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

        self.action_image_info = QAction(main_window)
        self.action_image_info.setObjectName("action_image_info")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/info.png"), QIcon.Normal, QIcon.Off)
        self.action_image_info.setIcon(icon)

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

        self.action_object_features = QAction(main_window)
        self.action_object_features.setObjectName("action_object_features")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/analyze.png"), QIcon.Normal, QIcon.Off)
        self.action_object_features.setIcon(icon)

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
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/watershed.png"), QIcon.Normal, QIcon.Off)
        self.action_watershed.setIcon(icon)

        self.action_svm_classification = QAction(main_window)
        self.action_svm_classification.setObjectName("action_svm_classification")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/svm.png"), QIcon.Normal, QIcon.Off)
        self.action_svm_classification.setIcon(icon)

        self.group_image_type = QActionGroup(self.menu_type)
        self.group_image_type.setObjectName("group_image_type")

        for img_type in IMAGE_TYPES:
            action = QAction(img_type, self.menu_type, checkable=True)
            self.menu_type.addAction(action)
            self.group_image_type.addAction(action)

        self.group_image_type.setExclusive(True)

        self.menu_type.addSeparator()
        self.action_color_depth_uint8 = QAction("8 bits per pixel", self.menu_type, checkable=True)
        self.menu_type.addAction(self.action_color_depth_uint8)

        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_undo)
        self.menu_file.addAction(self.action_cascade)
        self.menu_file.addAction(self.action_exit)

        self.menu_image.addMenu(self.menu_type)

        self.menu_image.addAction(self.action_rename)
        self.menu_image.addAction(self.action_duplicate)
        self.menu_image.addAction(self.action_image_info)
        self.menu_analyze.addAction(self.action_histogram)
        self.menu_analyze.addAction(self.action_profile)
        self.menu_analyze.addAction(self.action_object_features)
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

        self.menu_local_operations.addMenu(self.menu_edge_detection)
        self.menu_process.addMenu(self.menu_histogram)
        self.menu_process.addMenu(self.menu_point_operations)
        self.menu_process.addMenu(self.menu_local_operations)
        self.menu_process.addMenu(self.menu_segmentation)
        self.menu_process.addAction(self.action_svm_classification)
        self.menu_bar.addMenu(self.menu_file)
        self.menu_bar.addMenu(self.menu_image)
        self.menu_bar.addMenu(self.menu_analyze)
        self.menu_bar.addMenu(self.menu_process)
        self.menu_bar.addAction(self.action_panorama)
        self.menu_bar.addAction(self.action_program_info)

        self.file__toolbar.addAction(self.action_open)
        self.file__toolbar.addAction(self.action_save)
        self.file__toolbar.addAction(self.action_undo)
        self.file__toolbar.addAction(self.action_cascade)
        self.image__toolbar.addAction(self.action_rename)
        self.image__toolbar.addAction(self.action_duplicate)
        self.image__toolbar.addAction(self.action_image_info)
        self.analyze__toolbar.addAction(self.action_histogram)
        self.analyze__toolbar.addAction(self.action_profile)
        self.analyze__toolbar.addAction(self.action_object_features)

        self.retranslate_ui(main_window)
        QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        """
        Set the text and titles of the widgets.

        :param main_window: The main window of program
        :type main_window: :class:`main_window.MainWindow`
        """

        _translate = QCoreApplication.translate
        _main_title = "main_window"

        main_window.setWindowTitle(_translate(_main_title, "APO Image Processing"))
        self.menu_file.setTitle(_translate(_main_title, "File"))
        self.menu_image.setTitle(_translate(_main_title, "Image"))
        self.menu_analyze.setTitle(_translate(_main_title, "Analyze"))
        self.menu_process.setTitle(_translate(_main_title, "Process"))
        self.menu_type.setTitle(_translate(_main_title, "Type"))
        self.menu_histogram.setTitle(_translate(_main_title, "Histogram"))
        self.menu_point_operations.setTitle(_translate(_main_title, "Point Operations"))
        self.menu_local_operations.setTitle(_translate(_main_title, "Local Operations"))
        self.menu_segmentation.setTitle(_translate(_main_title, "Segmentation"))
        self.menu_edge_detection.setTitle(_translate(_main_title, "Edge Detection"))

        self.action_panorama.setText(_translate(_main_title, "Panorama"))
        self.action_program_info.setText(_translate(_main_title, "Info"))
        self.action_open.setText(_translate(_main_title, "Open"))
        self.action_save.setText(_translate(_main_title, "Save As"))
        self.action_undo.setText(_translate(_main_title, "Undo"))
        self.action_cascade.setText(_translate(_main_title, "Cascade"))
        self.action_exit.setText(_translate(_main_title, "Exit"))
        self.action_rename.setText(_translate(_main_title, "Rename"))
        self.action_duplicate.setText(_translate(_main_title, "Duplicate"))
        self.action_image_info.setText(_translate(_main_title, "Info"))
        self.action_histogram.setText(_translate(_main_title, "Histogram"))
        self.action_profile.setText(_translate(_main_title, "Plot Profile"))
        self.action_object_features.setText(_translate(_main_title, "Object Features"))
        self.action_normalize.setText(_translate(_main_title, "Normalization"))
        self.action_equalize.setText(_translate(_main_title, "Equalization"))
        self.action_negation.setText(_translate(_main_title, "Negation"))
        self.action_posterize.setText(_translate(_main_title, "Posterize"))
        self.action_image_calculator.setText(_translate(_main_title, "Image Calculator"))
        self.action_smooth.setText(_translate(_main_title, "Smooth"))
        self.action_edge_dt_dir.setText(_translate(_main_title, "Directional"))
        self.action_edge_dt_nondir.setText(_translate(_main_title, "Non-directional"))
        self.action_sharpen.setText(_translate(_main_title, "Sharpen"))
        self.action_convolve.setText(_translate(_main_title, "Convolve"))
        self.action_gray_morphology.setText(_translate(_main_title, "Gray Morphology"))
        self.action_threshold.setText(_translate(_main_title, "Threshold"))
        self.action_watershed.setText(_translate(_main_title, "Watershed"))
        self.action_svm_classification.setText(_translate(_main_title, "SVM Classification"))

        self.action_panorama.setStatusTip(_translate(_main_title, "Stitch images"))
        self.action_program_info.setStatusTip(_translate(_main_title, "About program"))
        self.action_open.setStatusTip(_translate(_main_title, "Open a new image"))
        self.action_save.setStatusTip(_translate(_main_title, "Save selected image"))
        self.action_undo.setStatusTip(_translate(_main_title, "Undo the last image changing."))
        self.action_cascade.setStatusTip(_translate(_main_title, "Arrange all the windows in a cascade pattern."))
        self.action_exit.setStatusTip(_translate(_main_title, "Exit the program"))
        self.action_rename.setStatusTip(_translate(_main_title, "Rename selected image"))
        self.action_duplicate.setStatusTip(_translate(_main_title, "Duplicate selected image"))
        self.action_image_info.setStatusTip(_translate(_main_title, "Show information about image"))
        self.action_histogram.setStatusTip(_translate(_main_title, "Show image histogram"))
        self.action_profile.setStatusTip(_translate(_main_title, "Plot image profile line"))
        self.action_object_features.setStatusTip(_translate(_main_title, "Show object features"))
        self.action_normalize.setStatusTip(_translate(_main_title, "Perform image histogram normalization"))
        self.action_equalize.setStatusTip(_translate(_main_title, "Perform image histogram Equalization"))
        self.action_negation.setStatusTip(_translate(_main_title, "Perform image negation"))
        self.action_posterize.setStatusTip(_translate(_main_title, "Perform image posterizing"))
        self.action_image_calculator.setStatusTip(_translate(_main_title, "Open image calculator"))
        self.action_smooth.setStatusTip(_translate(_main_title, "Perform image smoothing"))
        self.action_edge_dt_dir.setStatusTip(_translate(_main_title, "Perform directional edge detection"))
        self.action_edge_dt_nondir.setStatusTip(_translate(_main_title, "Perform local edge detection"))
        self.action_sharpen.setStatusTip(_translate(_main_title, "Perform image sharpening"))
        self.action_convolve.setStatusTip(_translate(_main_title, "Perform convolution operation"))
        self.action_gray_morphology.setStatusTip(_translate(_main_title, "Perfom morphology operation for grayscale"))
        self.action_threshold.setStatusTip(_translate(_main_title, "Perform image thresholding"))
        self.action_watershed.setStatusTip(_translate(_main_title, "Perform watershed segmentation"))
        self.action_svm_classification.setStatusTip(_translate(_main_title, "Perform support vector machine "
                                                                            "classification"))

        self.action_open.setShortcuts(QKeySequence.keyBindings(3))
        self.action_save.setShortcuts(QKeySequence.keyBindings(5))
        self.action_undo.setShortcuts(QKeySequence.keyBindings(11))
        self.action_rename.setShortcut("Ctrl+R")
        self.action_duplicate.setShortcut("Ctrl+D")
        self.action_image_info.setShortcut("Ctrl+F")
        self.action_histogram.setShortcut("Alt+S")
        self.action_profile.setShortcut("Alt+R")
        self.action_object_features.setShortcut("Alt+F")
