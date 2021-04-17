from PyQt5.QtGui import QImage, QPixmap

from src.constants import BYTES_PER_PIXEL_2_BW_FORMAT


class Operation:
    """The Operation class represents the base logic for operation classes."""

    def update_img_preview(self):
        """
        Update image preview window.

        - Convert new image data to :class:`PyQt5.QtGui.QImage`.
        - Reload the image to the preview window.
        """

        img_data = self.current_img_data
        height, width = img_data.shape[:2]

        if len(img_data.shape) == 2:
            pixel_bytes = img_data.dtype.itemsize
            image = QImage(img_data, width, height, BYTES_PER_PIXEL_2_BW_FORMAT[pixel_bytes])
        else:
            image = QImage(img_data, width, height, 3 * width, QImage.Format_BGR888)

        pixmap = QPixmap(image)
        self.label_image.setPixmap(pixmap)

    def accept_changes(self):
        """Accept changed image data to the original one."""

        self.img_data = self.current_img_data
        self.accept()
