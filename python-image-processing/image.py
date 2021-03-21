from hist_window import HistGraphicalSubWindow


class Image:
    def __init__(self, image, path):
        self.image = image
        self.path = path
        self.histogram_graphical = HistGraphicalSubWindow()

    def __calc_single_histogram(self):
        histogram = [0] * 256

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                pixel = self.image[w][h]
                histogram[pixel] += 1

        return {'b': histogram}

    def __calc_triple_histogram(self):
        histogram_rgb = [[0] * 256, [0] * 256, [0] * 256]

        for w in range(self.image.shape[0]):
            for h in range(self.image.shape[1]):
                for i in range(self.image.shape[2]):
                    pixel = self.image[w][h][i]
                    histogram_rgb[i][pixel] += 1

        return {'b': histogram_rgb[0], 'g': histogram_rgb[1], 'r': histogram_rgb[2]}

    def calc_histogram(self):
        if len(self.image.shape) == 2:
            return self.__calc_single_histogram()
        else:
            return self.__calc_triple_histogram()

    def create_hist_window(self):
        img_name = self.path.split("/")[-1]
        hist = self.calc_histogram()

        self.histogram_graphical.create_histogram_plot(hist, img_name)
