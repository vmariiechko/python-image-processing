
class Image:
    def __init__(self, img, sub_window):
        self.img = img
        self.sub_window = sub_window

    def __calc_single_histogram(self):
        histogram = [0] * 256

        for w in range(self.img.shape[0]):
            for h in range(self.img.shape[1]):
                pixel = self.img[w][h]
                histogram[pixel] += 1

        return histogram

    def __calc_triple_histogram(self):
        histogram_rgb = [[0] * 256, [0] * 256, [0] * 256]

        for w in range(self.img.shape[0]):
            for h in range(self.img.shape[1]):
                for i in range(self.img.shape[2]):
                    pixel = self.img[w][h][i]
                    histogram_rgb[i][pixel] += 1

        return histogram_rgb

    def calc_histogram(self):
        if len(self.img.shape) == 2:
            return self.__calc_single_histogram()
        else:
            return self.__calc_triple_histogram()
