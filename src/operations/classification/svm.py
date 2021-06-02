import matplotlib.pyplot as plt

from cv2 import (ml, imread, threshold, findContours, moments, contourArea, arcLength,
                 boundingRect, drawContours, cvtColor,
                 IMREAD_GRAYSCALE, TERM_CRITERIA_MAX_ITER, COLOR_GRAY2RGB)
from numpy import (array, matrix, ones, empty, delete, sqrt, pi,
                   vstack, hstack, concatenate, float32, int64)
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication, QSize

from src.constants import RETRIEVAL_MODES, APPROXIMATION_MODES
from ..operation import Operation
from .svm_ui import SVMUI

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import use

use("Qt5Agg")


class SVM(QDialog, Operation, SVMUI):
    """The SVM class implements a support vector machine classification."""

    def __init__(self, parent):
        """
        Create a new dialog window to perform SVM classification.

        Get image data from :param:`parent`.

        :param parent: The image to classificate
        :type parent: :class:`image.Image`
        """

        super().__init__()
        self.init_ui(self)

        self.img_data = parent.data.copy()
        self.current_img_data = None
        self.training_data = None
        self.training_shape = None
        self.training_labels = None
        self.svm = ml.SVM_create()
        self.svm_accuracy = None

        self.rbtn_show_confusion_matrix.clicked.connect(self.update_cm)

        self.train_SVM()
        self.make_predictions()
        self.__retranslate_ui()
        self.update_img_preview()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "SVM Classification"
        _svm_desc = "The SVM classifies objects belonging to the three classes: <b>rice, beans, lentils</b>"
        _training_data = f"The training data has {self.training_shape[1]} features (properties) " \
                         f"and {self.training_shape[0]} examples"
        _svm_accuracy = "Trained accuracy: " + str(self.svm_accuracy)
        _objects_colors = "The objects classified as rice have red contours, " \
                          "beans have green, and lentils have blue ones"

        self.setWindowTitle(_window_title)
        self.label_svm_desc.setText(_translate(_window_title, _svm_desc))
        self.label_training_data.setText(_translate(_window_title, _training_data))
        self.label_svm_accuracy.setText(_translate(_window_title, _svm_accuracy))
        self.label_objects_colors.setText(_translate(_window_title, _objects_colors))

    def get_features(self, img_data):
        """Return vector of properties for all found objects in the image."""

        _, img_data = threshold(img_data, 127, 255, 0)
        contours, _ = findContours(img_data, RETRIEVAL_MODES['List'], APPROXIMATION_MODES['Simple'])
        features = empty((29, 0))

        for contour in contours:
            obj_moments = moments(contour)
            moments_values = obj_moments.values()
            moments_values = array(list(moments_values)).flatten().reshape(-1, 1)

            area = contourArea(contour)
            perimeter = arcLength(contour, True)

            _, _, width, height = boundingRect(contour)
            aspect_ratio = float(width) / height
            rect_area = width * height
            extent = float(area) / rect_area
            equivalent_diameter = sqrt(4 * area / pi)

            feature_vector = array([area, perimeter, aspect_ratio, extent, equivalent_diameter]).reshape(-1, 1)
            feature_vector = vstack((moments_values, feature_vector))
            features = hstack((features, feature_vector))

        return features

    def get_labels(self, input_features, label_class=1):
        """Return the vector of labeled properties."""

        shape = input_features.shape
        out = ones((shape[1], 1))
        return out * label_class

    def update_training_data(self):
        """Calculate properties and labels of training data."""

        img = imread('icons/SVM_train_data/train_ryz.jpg', IMREAD_GRAYSCALE)
        features1 = self.get_features(img)
        features1 = delete(features1, features1.shape[1] - 1, axis=1)

        img = imread('icons/SVM_train_data/train_soczewica.jpg', IMREAD_GRAYSCALE)
        features2 = self.get_features(img)
        features2 = delete(features2, features2.shape[1] - 1, axis=1)

        img = imread('icons/SVM_train_data/train_fasola.jpg', IMREAD_GRAYSCALE)
        features3 = self.get_features(img)
        features3 = delete(features3, features3.shape[1] - 1, axis=1)

        self.training_data = float32(
            concatenate((features1, concatenate((features2, features3), axis=1)), axis=1).transpose()
        )

        self.training_shape = self.training_data.shape

        label1 = self.get_labels(features1, 1)
        label2 = self.get_labels(features2, 2)
        label3 = self.get_labels(features3, 3)

        self.training_labels = int64(concatenate((label1, concatenate((label2, label3)))))

    def train_SVM(self):
        """Train the SVM on calculated training data."""

        self.update_training_data()
        self.svm.setType(ml.SVM_C_SVC)
        self.svm.setKernel(ml.SVM_LINEAR)
        self.svm.setTermCriteria((TERM_CRITERIA_MAX_ITER, 1000, 1e-6))
        self.svm.train(self.training_data, ml.ROW_SAMPLE, self.training_labels)
        self.update_svm_accuracy()

    def update_svm_accuracy(self):
        """Calculate SVM accuracy and confusion matrix."""

        prediction = self.svm.predict(self.training_data)[1]
        self.svm_accuracy = accuracy_score(self.training_labels, prediction)
        self.cm_display = ConfusionMatrixDisplay(confusion_matrix(self.training_labels, prediction),
                                                 display_labels=['rice', 'lentils', 'beans'])
        self.cm_display.plot()
        self.cm_canvas = FigureCanvas(plt.gcf())
        self.layout_preview.addWidget(self.cm_canvas)
        self.cm_canvas.draw()
        self.cm_canvas.setVisible(False)

    def make_predictions(self):
        """Predict object classification."""

        img_data = self.img_data.copy()
        features = self.get_features(img_data)

        _, img_data = threshold(img_data, 127, 255, 0)
        contours, _ = findContours(img_data, RETRIEVAL_MODES['List'], APPROXIMATION_MODES['None'])
        img_data = cvtColor(img_data, COLOR_GRAY2RGB)

        for i in range(len(contours)):
            feature_predict = float32(features[:, i].reshape(-1, 1).transpose())
            response = self.svm.predict(feature_predict)[1]
            contour = contours[i]

            if response == 1:
                drawContours(img_data, [contour], 0, (0, 255, 0), 3)
            elif response == 2:
                drawContours(img_data, [contour], 0, (0, 0, 255), 3)
            elif response == 3:
                drawContours(img_data, [contour], 0, (255, 0, 0), 3)
            else:
                drawContours(img_data, [contour], 0, (255, 255, 255), 3)

        self.current_img_data = img_data

    def update_cm(self):
        """Update confusion matrix canvas visibility whenever :attr:`rbtn_show_confusion_matrix` clicked."""

        if self.rbtn_show_confusion_matrix.isChecked():
            self.cm_canvas.setVisible(True)
            self.resize(self.layout.sizeHint() + QSize(self.cm_canvas.size().width(), 0))
        else:
            self.cm_canvas.setVisible(False)
            self.resize(self.layout.sizeHint() - QSize(self.cm_canvas.size().width(), 0))
            self.adjustSize()
