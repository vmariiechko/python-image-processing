from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from ..operation import Operation
from .morphology_ui import MorphologyUI


class Morphology(QDialog, Operation, MorphologyUI):

    def __init__(self, parent):

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.img_data = parent.img_data.copy()
        self.current_img_data = None

        self.cb_operator.activated[str].connect(self.update_img_preview)
        self.cb_structure_element.activated[str].connect(self.update_img_preview)
        self.cb_border_type.activated[str].connect(self.update_img_preview)

        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Morphology"

        self.setWindowTitle(_window_title)
        self.label_operator.setText(_translate(_window_title, "Operator:"))
        self.label_structure_element.setText(_translate(_window_title, "Structure element:"))
        self.label_kernel_size.setText(_translate(_window_title, "Kernel size:"))
        self.label_border_type.setText(_translate(_window_title, "Border type:"))

    def calc_morphology(self, operator, structure_element, border_type):
        pass

    def update_img_preview(self):

        operator = self.cb_operator.currentText()
        structure_element = self.cb_structure_element.currentText()
        border_type = self.cb_border_type.currentText()

        # self.current_img_data = self.calc_morphology(operator, structure_element, border_type)
        self.current_img_data = self.img_data
        super().update_img_preview()
