from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QDialogButtonBox, QAbstractItemView, QAbstractScrollArea)
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from src.operations.form_ui import FormUI
from src.constants import RETRIEVAL_MODES, APPROXIMATION_MODES


class ObjectPropertiesUI(FormUI):
    """Build UI for :class:`object_properties.ObjectProperties`."""

    def init_ui(self, object_properties, height):
        """
        Create user interface for :class:`object_properties.ObjectProperties`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param object_properties: The dialog object properties window
        :type object_properties: :class:`object_properties.ObjectProperties`
        :param height: The height of the image
        :type height: int
        """

        self.form_ui(self)
        row_count = 30
        object_properties.setObjectName("object_properties")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/analyze.png"), QIcon.Normal, QIcon.Off)
        object_properties.setWindowIcon(icon)

        self.label_method = QLabel(object_properties)
        self.label_method.setObjectName("label_method")

        self.cb_method = QComboBox(object_properties)
        self.cb_method.addItems(list(APPROXIMATION_MODES.keys()))
        self.cb_method.setObjectName("cb_method")

        self.label_mode = QLabel(object_properties)
        self.label_mode.setObjectName("label_mode")

        self.cb_mode = QComboBox(object_properties)
        self.cb_mode.addItems(list(RETRIEVAL_MODES.keys()))
        self.cb_mode.setObjectName("cb_mode")

        self.label_objects = QLabel(object_properties)
        self.label_objects.setObjectName("label_objects")

        self.cb_objects = QComboBox(object_properties)
        self.cb_objects.setObjectName("cb_objects")

        self.layout_form.addRow(self.label_method, self.cb_method)
        self.layout_form.addRow(self.label_mode, self.cb_mode)
        self.layout_form.addRow(self.label_objects, self.cb_objects)

        self.layout_preview = QHBoxLayout(object_properties)
        self.layout_preview.setObjectName("layout_preview")

        self.label_image = QLabel(object_properties)
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

        self.preview_widget = QWidget(object_properties)
        self.preview_widget.setObjectName("preview_widget")
        self.preview_widget.setLayout(self.layout_preview)

        self.button_box = QDialogButtonBox(object_properties)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.accepted.connect(object_properties.accept)
        self.button_box.setObjectName("button_box")

        self.layout = QVBoxLayout()
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        object_properties.setWindowFlags(object_properties.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        object_properties.setLayout(self.layout)
        QMetaObject.connectSlotsByName(object_properties)
