# Map ndarray.dtype.itemsize to QImage bytes per pixel format for grayscale image
bytes_per_pixel = {
    1: QImage.Format_Grayscale8,
    2: QImage.Format_Grayscale16
}