from cv2 import BORDER_ISOLATED, BORDER_REFLECT, BORDER_REPLICATE
from PyQt5.QtGui import QImage

# Map amout of bytes per one pixel to QImage black&white image format
BYTES_PER_PIXEL_2_BW_FORMAT = {
    1: QImage.Format_Grayscale8,
    2: QImage.Format_Grayscale16,
}

# Map names of border types to their number
BORDER_TYPES = {
    "Isolated": BORDER_ISOLATED,
    "Reflect": BORDER_REFLECT,
    "Replicate": BORDER_REPLICATE,
}
