from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QDialogButtonBox, QAbstractItemView, QAbstractScrollArea)
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from src.operations.form_ui import FormUI
from src.constants import RETRIEVAL_MODES, APPROXIMATION_MODES


class VectorPropertiesUI(FormUI):
    """Build UI for :class:`vector_properties.VectorProperties`."""

    def init_ui(self, vector_properties, height):
        """
        Create user interface for :class:`vector_properties.VectorProperties`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param vector_properties: The dialog vector properties window
        :type vector_properties: :class:`vector_properties.VectorProperties`
        :param height: The height of the image
        :type height: int
        """

        self.form_ui(self)
        row_count = 30
        vector_properties.setObjectName("posterize")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/analyze.png"), QIcon.Normal, QIcon.Off)
        vector_properties.setWindowIcon(icon)

        self.label_method = QLabel(vector_properties)
        self.label_method.setObjectName("label_method")

        self.cb_method = QComboBox(vector_properties)
        self.cb_method.addItems(list(APPROXIMATION_MODES.keys()))
        self.cb_method.setObjectName("cb_method")

        self.label_mode = QLabel(vector_properties)
        self.label_mode.setObjectName("label_mode")

        self.cb_mode = QComboBox(vector_properties)
        self.cb_mode.addItems(list(RETRIEVAL_MODES.keys()))
        self.cb_mode.setObjectName("cb_mode")

        self.label_objects = QLabel(vector_properties)
        self.label_objects.setObjectName("label_objects")

        self.cb_objects = QComboBox(vector_properties)
        self.cb_objects.setObjectName("cb_objects")

        self.layout_form.addRow(self.label_method, self.cb_method)
        self.layout_form.addRow(self.label_mode, self.cb_mode)
        self.layout_form.addRow(self.label_objects, self.cb_objects)

        self.layout_preview = QHBoxLayout(vector_properties)
        self.layout_preview.setObjectName("layout_preview")

        self.label_image = QLabel(vector_properties)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setObjectName("label_image")

        self.table_widget = QTableWidget()
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_widget.setMaximumHeight(height)
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(row_count)
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("Property"))
        self.table_widget.setHorizontalHeaderItem(1, QTableWidgetItem("Value"))

        for i in range(row_count):
            self.table_widget.setVerticalHeaderItem(i, QTableWidgetItem())

        self.layout_preview.addWidget(self.label_image)
        self.layout_preview.addWidget(self.table_widget)

        self.preview_widget = QWidget(vector_properties)
        self.preview_widget.setObjectName("preview_widget")
        self.preview_widget.setLayout(self.layout_preview)

        self.button_box = QDialogButtonBox(vector_properties)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.accepted.connect(vector_properties.accept)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        vector_properties.setWindowFlags(vector_properties.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        vector_properties.setLayout(self.layout)
        QMetaObject.connectSlotsByName(vector_properties)
