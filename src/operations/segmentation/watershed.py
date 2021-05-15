from cv2 import (cvtColor, threshold, morphologyEx, distanceTransform, subtract,
                 connectedComponents, watershed, applyColorMap, addWeighted,
                 COLOR_BGR2GRAY, COLORMAP_JET, DIST_L2,
                 THRESH_BINARY_INV, THRESH_OTSU)
from numpy import ones, uint8, stack, max
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from src.constants import MORPH_OPERATIONS
from ..operation import Operation
from .watershed_ui import WatershedUI


class Watershed(QDialog, Operation, WatershedUI):
    """The Watershed class implements a watershed segmentation."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform watershed.

        Get image data from :param:`parent`.
        Calculate watershed for image data with different previews.
        Set objects count to label.

        :param parent: The image to watershed
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        self.img_data = parent.img_data.copy()
        self.current_img_data = None

        obj_count, self.preview = self.calc_watershed(self.img_data)
        self.label_objects_count_value.setText(str(obj_count))

        self.cb_watershed_preview.activated[str].connect(self.update_img_preview)
        self.rbtn_show_hist.clicked.connect(self.update_hist)

        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Watershed"

        self.setWindowTitle(_window_title)
        self.label_objects_count_txt.setText(_translate(_window_title, "Objects Count:"))
        self.label_watershed_preview.setText(_translate(_window_title, "Watershed Preview:"))

    @staticmethod
    def calc_watershed(img_color):
        """
        Calculate watershed segmentation with different previews.

        There are 4 previews of segmented objects:
            - Color image.
            - Grayscale image.
            - Pseudocolor.
            - Blended.

        :param img_color: The image data to perform watershed
        :type img_color: class:`numpy.ndarray`
        :return: The pair: objects count and dictionary with available previews
        :rtype: tuple[int, dict]
        """

        # Convert to the grayscale image
        img_gray = cvtColor(img_color, COLOR_BGR2GRAY)

        # Initial detection of objects
        _, thresh_otsu = threshold(img_gray, 0, 255, THRESH_BINARY_INV + THRESH_OTSU)

        # Noise reduction
        kernel = ones((3, 3), "uint8")
        opening = morphologyEx(thresh_otsu, MORPH_OPERATIONS["Open"], kernel, iterations=1)

        # Detect unequivocal background areas
        bg_area = morphologyEx(opening, MORPH_OPERATIONS["Dilate"], kernel, iterations=1)

        # Detect unequivocal objects background
        dist_transform = distanceTransform(opening, DIST_L2, 5)
        _, obj_area = threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
        obj_area = uint8(obj_area)

        # Calculate 'uncertain' areas
        uncertain = subtract(bg_area, obj_area)

        # Objects labeling
        _, markers = connectedComponents(obj_area)
        markers += 1

        # Labeling uncertain areas as zero
        markers[uncertain == 255] = 0

        markers2 = watershed(img_color, markers)
        obj_count = max(markers2)

        # Add object border lines for color and grayscale image data
        img_gray[markers2 == -1] = 255
        img_color[markers2 == -1] = [0, 0, 255]

        pseudocolor = applyColorMap(uint8(markers2 * 10), COLORMAP_JET)
        blended = addWeighted(stack((img_gray,) * 3, axis=-1), 0.7, pseudocolor, 0.5, -1)

        preview = {
            "Color Image": img_color,
            "Grayscale Image": img_gray,
            "Pseudocolor": pseudocolor,
            "Blended": blended,
        }

        return obj_count, preview

    def update_img_preview(self):
        """
        Update image preview window.

        - Select image preview based on chosen preview.
        - Reload image preview using the base :class:`operation.Operation` method.
        """

        preview_type = self.cb_watershed_preview.currentText()

        self.current_img_data = self.preview[preview_type]
        super().update_img_preview()
