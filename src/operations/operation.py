from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QSize

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

        scale = 1
        if width > 1200 or height > 1200:
            scale = 0.4
        elif width > 800 or height > 800:
            scale = 0.6
        elif width > 300 and height > 300:
            scale = 0.8

        if len(img_data.shape) == 2:
            pixel_bytes = img_data.dtype.itemsize
            image = QImage(img_data, width, height, BYTES_PER_PIXEL_2_BW_FORMAT[pixel_bytes])
        else:
            image = QImage(img_data, width, height, 3 * width, QImage.Format_BGR888)

        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(scale * pixmap.size())
        self.label_image.setPixmap(pixmap)

        # Prevent from calculating histogram for images with color depth higher than 8-bit
        if img_data.dtype.itemsize > 1:
            self.rbtn_show_hist.setEnabled(False)
        else:
            self.hist_canvas.axes.clear()
            self.hist_canvas.axes.hist(img_data.ravel(), 256, [0, 256])
            self.hist_canvas.draw()

    def update_hist(self):
        """Update histogram canvas visibility whenever :attr:`rbtn_show_hist` clicked."""

        if self.rbtn_show_hist.isChecked():
            self.hist_canvas.setVisible(True)
            self.resize(self.layout.sizeHint() + QSize(self.hist_canvas.size().width(), 0))
        else:
            self.hist_canvas.setVisible(False)
            self.resize(self.layout.sizeHint() - QSize(self.hist_canvas.size().width(), 0))
            self.adjustSize()

    def accept_changes(self):
        """Accept changed image data to the original one."""

        self.img_data = self.current_img_data
        self.accept()
