from collections import OrderedDict

from cv2 import (findContours, cvtColor, drawContours, moments, contourArea, arcLength,
                 threshold, boundingRect, convexHull, COLOR_GRAY2RGB)
from numpy import sqrt, pi
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QCoreApplication

from .vector_properties_ui import VectorPropertiesUI
from src.constants import BYTES_PER_PIXEL_2_BW_FORMAT, RETRIEVAL_MODES, APPROXIMATION_MODES


class VectorProperties(QDialog, VectorPropertiesUI):

    def __init__(self, parent):
        """
        Create a new dialog window to analyze vector properties.

        Get image data from :param:`parent` and threshold it.

        :param parent: The image to analyze
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self, parent.data.shape[0])
        self.__retranslate_ui()

        _, self.img_data = threshold(parent.data.copy(), 127, 255, 0)
        self.contours = None
        self.selected_object = None

        self.cb_objects.activated[str].connect(self.update_selected_object)
        self.cb_mode.activated[str].connect(self.find_contours)
        self.cb_method.activated[str].connect(self.find_contours)

        self.find_contours()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Vector Properties"

        self.setWindowTitle(_window_title)
        self.label_method.setText(_translate(_window_title, "Approximation method:"))
        self.label_mode.setText(_translate(_window_title, "Retrieval mode:"))
        self.label_objects.setText(_translate(_window_title, "Objects:"))

    def find_contours(self):
        """Calculate objects' contours."""

        mode = RETRIEVAL_MODES[self.cb_mode.currentText()]
        method = APPROXIMATION_MODES[self.cb_method.currentText()]
        self.contours, _ = findContours(self.img_data, mode, method)
        self.cb_objects.clear()
        self.cb_objects.addItems([str(i) for i in range(len(self.contours))])
        self.update_selected_object()

    def calc_moments(self):
        """Calculate all the moments in sorted order."""

        obj_moments = moments(self.selected_object)
        obj_moments = {key.upper(): value for key, value in obj_moments.items()}
        return OrderedDict(sorted(obj_moments.items()))

    def calc_properties(self):
        """
        Calculate vector properties based on selected object contour.

        Calculated vector properties:
            - area;
            - perimeter;
            - aspect radio;
            - extent;
            - solidity;
            - equivalent diameter;
            - moments (up to the 3rd order).

        :return: The vector properties
        :rtype: dict
        """

        _, _, width, height = boundingRect(self.selected_object)
        hull = convexHull(self.selected_object)
        area = contourArea(self.selected_object)
        hull_area = contourArea(hull)
        rect_area = width * height
        perimeter = arcLength(self.selected_object, True)
        aspect_ratio = float(width) / height
        extent = float(area) / rect_area
        solidity = float(area) / hull_area
        equivalent_diameter = sqrt(4 * area / pi)
        obj_moments = self.calc_moments()

        properties = {
            "Area": area,
            "Perimeter": perimeter,
            "Aspect ratio": aspect_ratio,
            "Extent": extent,
            "Solidity": solidity,
            "Equivalent diameter": equivalent_diameter,
            **obj_moments
        }
        return properties

    def update_selected_object(self):
        """Update the contour of the selected object whenever changed."""

        obj_num = int(self.cb_objects.currentText())
        self.selected_object = self.contours[obj_num]
        self.update_properties()

    def update_properties(self):
        """Update the properties table whenever the form changed."""

        properties = self.calc_properties()
        for row_num, attribute in enumerate(properties.items()):
            self.table_widget.setItem(row_num, 0, QTableWidgetItem(str(attribute[0])))
            self.table_widget.setItem(row_num, 1, QTableWidgetItem(str(attribute[1])))
        self.table_widget.resizeColumnsToContents()
        self.update_img_preview()

    def update_img_preview(self):
        """
        Update image preview window.

        - Draw contours for the selected object.
        - Convert new image data to :class:`PyQt5.QtGui.QImage`.
        - Reload the image to the preview window.
        """

        img_data = self.img_data
        height, width = img_data.shape[:2]

        img_data = cvtColor(img_data, COLOR_GRAY2RGB)
        drawContours(img_data, [self.selected_object], 0, (0, 0, 255, 3), 2)

        if len(img_data.shape) == 2:
            pixel_bytes = img_data.dtype.itemsize
            image = QImage(img_data, width, height, BYTES_PER_PIXEL_2_BW_FORMAT[pixel_bytes])
        else:
            image = QImage(img_data, width, height, 3 * width, QImage.Format_BGR888)

        pixmap = QPixmap(image)
        self.label_image.setPixmap(pixmap)
