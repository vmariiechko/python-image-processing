from numpy import array, flip


class ImageBmp:
    """The ImageBmp class implements manual reading of image data for .bmp images."""

    def __init__(self, raw):
        """Create a new BMP image."""

        self._raw = raw
        self._pixels = self.get_pixels()

    @staticmethod
    def get_type(max_pixel_value):
        """
        Return the image data type.

        :param max_pixel_value: The maximum pixel value
        :type max_pixel_value: int
        :return: The name of :class:`numpy.dtype`. Can be "uint8", "uint16", "uint32"
        :rtype: str
        """

        if max_pixel_value < 256:
            return "uint8"
        elif max_pixel_value < 65536:
            return "uint16"
        else:
            return "uint32"

    @staticmethod
    def get_channels_num(bits_per_pixel):
        """
        Return number of channels in the image

        :param bits_per_pixel: The number of bits per pixel, gets from :meth:`get_bits_per_pixel`
        :type bits_per_pixel: int
        :return: The number of channels
        :rtype: int
        """

        if bits_per_pixel < 8:
            return 1
        return bits_per_pixel // 8

    @property
    def pixels(self):
        """Get :attr:`_pixels`."""

        return self._pixels

    def get_data_offset(self):
        """Return the starting address of the byte where is the pixel array (image data)."""

        return int.from_bytes(self._raw[10:14], byteorder="little")

    def get_bits_per_pixel(self):
        """Return the number of bits per pixel (color depth)."""

        return int.from_bytes(self._raw[28:30], byteorder="little")

    def get_width(self):
        """Return the bitmap image width in pixels."""

        return int.from_bytes(self._raw[18:22], byteorder="little")

    def get_height(self):
        """Return the bitmap image height in pixels."""

        return int.from_bytes(self._raw[22:26], byteorder="little")

    def get_image_compression(self):
        """Return the used compression method. 0 - most common BI_RGB."""

        return int.from_bytes(self._raw[30:34], byteorder="little")

    def get_image_size(self):
        """Return the size of the raw bitmap data."""

        return int.from_bytes(self._raw[34:38], byteorder="little")

    def get_color_table(self):
        """Get the color table for the 8-bit and lower image."""

        bits_per_pixel = self.get_bits_per_pixel()
        if bits_per_pixel <= 8:
            return self._raw[54:self.get_data_offset()]
        else:
            return 0

    def get_raw_pixel_data(self):
        """Return the raw pixel data of the image."""

        return self._raw[self.get_data_offset():]

    def get_pixels(self):
        """
        Extract pixel data from the image and shape it.

        :return: The image pixel data
        """

        assert self.get_image_compression() == 0, AssertionError("Can't read compressed image")

        width = self.get_width()
        height = self.get_height()
        data_start = self.get_data_offset()
        channels_num = self.get_channels_num(self.get_bits_per_pixel())

        padding = width & 3
        data_end = data_start + (width * height * 3) + (height * padding)

        data = array(list(self._raw[data_start:data_end]))
        lines = data.reshape(height, -1)
        img_data_type = self.get_type(data.max())

        if channels_num == 1:
            # BMP pixel data stores in reversed order
            pixels = flip(lines, 0)
        else:
            # Reshape multi-channel image to a 2D array,
            # where each element has an array of pixel value for each channel
            pixels = array([line[:width * channels_num].reshape(width, channels_num) for line in reversed(lines)])

        return pixels.astype(img_data_type)
