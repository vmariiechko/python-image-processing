from hist_window import HistSubWindow


class Image:
    def __init__(self, image, path):
        self.image = image
        self.path = path
        self.histogram = HistSubWindow()

    def __calc_single_histogram(self):
        histogram = [[0] * 256]

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                pixel = self.image[w][h]
                histogram[0][pixel] += 1

        return histogram, 'b'

    def __calc_triple_histogram(self):
        histogram_rgb = [[0] * 256, [0] * 256, [0] * 256]

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                for i in range(self.image.shape[2]):
                    pixel = self.image[w][h][i]
                    histogram_rgb[i][pixel] += 1

        return histogram_rgb, ('b', 'g', 'r')

    def calc_histogram(self):
        if len(self.image.shape) == 2:
            return self.__calc_single_histogram()
        else:
            return self.__calc_triple_histogram()

    def create_hist_window(self):
        self.histogram.create_histogram_plot(self.calc_histogram(), self.path.split("/")[-1])
