from cv2 import (COLOR_BGR2GRAY, COLOR_GRAY2BGR, COLOR_BGRA2BGR,
                 BORDER_ISOLATED, BORDER_REFLECT, BORDER_REPLICATE,
                 MORPH_RECT, MORPH_ELLIPSE, MORPH_CROSS,
                 MORPH_ERODE, MORPH_DILATE,
                 MORPH_OPEN, MORPH_CLOSE, MORPH_TOPHAT, MORPH_BLACKHAT,
                 RETR_EXTERNAL, RETR_LIST, RETR_CCOMP, RETR_TREE,
                 CHAIN_APPROX_NONE, CHAIN_APPROX_SIMPLE, CHAIN_APPROX_TC89_L1, CHAIN_APPROX_TC89_KCOS)
from PyQt5.QtGui import QImage

# List of available image types for conversion
IMAGE_TYPES = [
    "Grayscale",
    "BGR-Color",
]

# Map image types to conversion codes
COLOR_CONVERSION_CODES = {
    "Grayscale": COLOR_BGR2GRAY,
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

# Map names of retrieval modes in finding contours to their number
RETRIEVAL_MODES = {
    "List": RETR_LIST,
    "Two-level Hierarchy": RETR_CCOMP,
    "External": RETR_EXTERNAL,
    "Tree": RETR_TREE,
}

# Map names of contour approximation modes to their number
APPROXIMATION_MODES = {
    "None": CHAIN_APPROX_NONE,
    "Simple": CHAIN_APPROX_SIMPLE,
    "TC89 L1": CHAIN_APPROX_TC89_L1,
    "TC89 KCOS": CHAIN_APPROX_TC89_KCOS,
}
