from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from threshold_ui import ThresholdUI


class Threshold(QDialog, ThresholdUI):

    def __init__(self, parent=None):
        super().__init__()
        self.init_ui(self)
        self.setWindowTitle("Threshold")

        self.img_data = parent.image.copy()
        self.new_img_data = None
        self.color_depth = parent.color_depth - 1

        self.threshold_slider.setMaximum(self.color_depth)
        self.threshold_slider.setProperty("value", self.color_depth // 2)

        self.threshold_slider.valueChanged.connect(self.update_thresh_value)
        self.threshold_slider.sliderReleased.connect(self.update_img_preview)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(self.accept_changes)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.update_thresh_value()
        self.update_img_preview()

    def update_thresh_value(self):
        self.label_thresh_value.setText("Threshold value: "
                                        + str(self.threshold_slider.value()))

    def calc_threshold(self, thresh_value):
        img_data = self.img_data.copy()

        for w in range(img_data.shape[0]):
            for h in range(img_data.shape[1]):
                img_data[w][h] = self.color_depth - 1 if img_data[w][h] > thresh_value else 0

        return img_data

    def update_img_preview(self):
        thresh_value = self.threshold_slider.value()
        img_data = self.calc_threshold(thresh_value)

        height, width = img_data.shape[:2]

        if img_data.dtype.itemsize == 1:
            image = QImage(img_data, width, height, QImage.Format_Grayscale8)
        else:
            image = QImage(img_data, width, height, QImage.Format_Grayscale16)

        pixmap = QPixmap(image)
        self.label_image.setPixmap(pixmap)
        self.new_img_data = img_data

    def accept_changes(self):
        self.img_data = self.new_img_data
        self.accept()
