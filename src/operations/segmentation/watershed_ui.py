from PyQt5.QtWidgets import QLabel, QComboBox
from PyQt5.QtCore import QMetaObject

from ..operation_ui import OperationUI
from ..form_ui import FormUI


class WatershedUI(OperationUI, FormUI):
    """Build UI for :class:`watershed.Watershed`."""

    def init_ui(self, watershed):
        """
        Create user interface for :class:`watershed.Watershed`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param watershed: The dialog watershed window
        :type watershed: :class:`watershed.Watershed`
        """

        self.operation_ui(self)
        self.form_ui(self)
        watershed.setObjectName("watershed")

        self.label_objects_count_txt = QLabel(watershed)
        self.label_objects_count_txt.setObjectName("label_objects_count_txt")

        self.label_objects_count_value = QLabel(watershed)
        self.label_objects_count_value.setObjectName("label_objects_count_value")

        self.label_watershed_preview = QLabel(watershed)
        self.label_watershed_preview.setObjectName("label_watershed_preview")

        self.cb_watershed_preview = QComboBox(watershed)
        self.cb_watershed_preview.addItems(["Color Image", "Grayscale Image", "Pseudocolor", "Blended"])
        self.cb_watershed_preview.setObjectName("cb_watershed_preview")

        self.layout_form.addRow(self.label_objects_count_txt, self.label_objects_count_value)
        self.layout_form.addRow(self.label_watershed_preview, self.cb_watershed_preview)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        watershed.setLayout(self.layout)
        QMetaObject.connectSlotsByName(watershed)
