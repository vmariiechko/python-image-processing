from cv2 import (COLOR_BGR2GRAY, COLOR_GRAY2BGR, COLOR_BGRA2BGR,
                 BORDER_ISOLATED, BORDER_REFLECT, BORDER_REPLICATE,
                 MORPH_RECT, MORPH_ELLIPSE, MORPH_CROSS,
                 MORPH_ERODE, MORPH_DILATE,
                 MORPH_OPEN, MORPH_CLOSE, MORPH_TOPHAT, MORPH_BLACKHAT)
from PyQt5.QtGui import QImage

# List of available image types for conversion
IMAGE_TYPES = [
    "8-bit",
    "BGR-Color",
]

# Map image types to conversion codes
COLOR_CONVERSION_CODES = {
    "8-bit": COLOR_BGR2GRAY,
    "BGR-Color": COLOR_GRAY2BGR,
    "BGRA2BGR": COLOR_BGRA2BGR,
}

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

# Map names of the shape of structuring elements to their number
MORPH_SHAPES = {
    "Rectangle": MORPH_RECT,
    "Ellipse": MORPH_ELLIPSE,
    "Cross": MORPH_CROSS,
}

# Map names of morphological operations to their number
MORPH_OPERATIONS = {
    "Erode": MORPH_ERODE,
    "Dilate": MORPH_DILATE,
    "Open": MORPH_OPEN,
    "Close": MORPH_CLOSE,
    "Top Hat": MORPH_TOPHAT,
    "Black Hat": MORPH_BLACKHAT,
}
