from cv2 import getStructuringElement, morphologyEx
from numpy import uint8, add, r_
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from src.constants import BORDER_TYPES, MORPH_SHAPES, MORPH_OPERATIONS
from ..operation import Operation
from .morphology_ui import MorphologyUI


class Morphology(QDialog, Operation, MorphologyUI):
    """The Morphology class implements a morphological transformation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform morphology.

        Get image data from :param:`parent`.
        Set kernel size maximum value.

        :param parent: The image to morphology
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.img_data = parent.img_data.copy()
        self.current_img_data = None
        self.structuring_element = None

        self.sb_kernel_size.setMaximum(99)

        self.cb_operation.activated[str].connect(self.update_img_preview)
        self.cb_border_type.activated[str].connect(self.update_img_preview)
        self.cb_struct_element_shape.activated[str].connect(self.update_structuring_element)
        self.sb_kernel_size.valueChanged.connect(self.update_structuring_element)
        self.sb_iterations.valueChanged.connect(self.update_img_preview)

        self.update_structuring_element()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Morphology"

        self.setWindowTitle(_window_title)
        self.label_operation.setText(_translate(_window_title, "Operation:"))
        self.label_struct_element_shape.setText(_translate(_window_title, "Shape of structuring element:"))
        self.label_kernel_size.setText(_translate(_window_title, "Kernel size:"))
        self.label_iterations.setText(_translate(_window_title, "Iterations:"))
        self.label_border_type.setText(_translate(_window_title, "Border type:"))

    def update_structuring_element(self):
        """Update structuring element whenever shape or kernel size changed."""

        shape = self.cb_struct_element_shape.currentText()
        ksize = self.sb_kernel_size.value()

        if ksize % 2 == 0:
            ksize -= 1
            self.sb_kernel_size.setValue(ksize)

        if shape == "Diamond":
            self.structuring_element = uint8(add.outer(*[r_[:ksize, ksize:-1:-1]]*2) >= ksize)
        else:
            self.structuring_element = getStructuringElement(MORPH_SHAPES[shape], (ksize, ksize))

        self.update_img_preview()

    def calc_morphology(self, operation_name, border, iterations):
        """
        Calculate morphological transformation based on structuring element,
        operation and border type

        :param operation_name: The type of morphological operation
        :type operation_name: str
        :param border: The border type for convolution, defined in BORDER_TYPES
        :type border: str
        :param iterations: The number of times to execute operation
        :type iterations: str
        :return: The new morphological transformed image data
        :rtype: class:`numpy.ndarray`
        """

        return morphologyEx(self.img_data, MORPH_OPERATIONS[operation_name], self.structuring_element,
                            iterations=iterations, borderType=BORDER_TYPES[border])

    def update_img_preview(self):
        """
        Update image preview window.

        - Calculate morphological transformation.
        - Reload histogram preview.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        operation_name = self.cb_operation.currentText()
        border_type = self.cb_border_type.currentText()
        iterations = self.sb_iterations.value()

        self.current_img_data = self.calc_morphology(operation_name, border_type, iterations)

        self.hist_canvas.axes.clear()
        self.hist_canvas.axes.hist(self.current_img_data.ravel(), 256, [0, 256])
        self.hist_canvas.draw()

        super().update_img_preview()
