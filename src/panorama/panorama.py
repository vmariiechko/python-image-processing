from imutils import grab_contours
from cv2 import (Stitcher_create, cvtColor, threshold, copyMakeBorder, findContours,
                 contourArea, boundingRect, rectangle, countNonZero, erode, subtract,
                 COLOR_BGR2GRAY, THRESH_BINARY, BORDER_CONSTANT, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
from numpy import zeros
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

from .stitcher import Stitcher
from .panorama_ui import ImagePanoramaUI


class ImagePanorama(QDialog, ImagePanoramaUI):
    """The ImagePanorama class represents stitching between chosen images."""

    ERROR_MESSAGES = {
        1: "Need more input images to construct the panorama,\n"
           "or try to reverse the image order on the right list\n"
           "using the 'Up' and 'Down' buttons",
        2: "RANSAC homography estimation failed:\n"
           "You may need more images or your images don't have enough distinguishing,\n"
           "unique texture/objects for keypoints to be accurately matched",
        3: "Failed to properly estimate camera intrinsics/extrinsics from the input images",
        4: "The Manual mode stitches only two images",
    }

    def __init__(self, images):
        """
        Create a new dialog window to perform image stitching.

        Fill out left list with image names from :param:`images`

        :param images: The images to perform stitching, dict[img_name:data]
        :type images: dict
        """

        super().__init__()
        self.init_ui(self)
        self.__retranslate_ui()

        for i in images.keys():
            self.left_list.addItem(i)

        self.images = images.copy()
        self.pano_name = "panorama"
        self.pano_data = None

        self.edit_pano_name.setText(self.pano_name)

        self.update_button_status()
        self.set_widget_connections()

    def __retranslate_ui(self):
        """Set the text and titles of the widgets."""

        _translate = QCoreApplication.translate
        _window_title = "Image Panorama"

        self.setWindowTitle(_window_title)
        self.label_mode.setText(_translate(_window_title, "Mode:"))
        self.label_pano_name.setText(_translate(_window_title, "Image Name:"))
        self.label_left_list.setText(_translate(_window_title, "All images"))
        self.label_right_list.setText(_translate(_window_title, "Images to stitch"))

    def get_selected_images(self):
        """Return image data from the list on the right side."""

        images_data = []
        for i in range(self.right_list.count()):
            img_name = self.right_list.takeItem(0).text()
            images_data.append(self.images[img_name])
            self.left_list.addItem(img_name)

        return images_data

    def stitch_manually(self, images_data):
        """
        Stitch two images using manual implementation.
        See :class:`Stitcher` for more information.

        :param images_data: The two images to stitch
        :type images_data: list
        :return: The status of stitching and image panorama
        :rtype: tuple
        """

        if len(images_data) != 2:
            return 4, None

        status, stitched = Stitcher(images_data, 2000).stitch()

        return status, stitched

    def stitch_built_in(self, images_data):
        """
        Stitch images with built-in OpenCV .stitch() method.

        There is an additional mode to crop the stitched data,
        which cuts out black borders.

        :param images_data: The images to stitch
        :type images_data: list
        :return: The status of stitching and image panorama
        :rtype: tuple
        """

        status, stitched = Stitcher_create().stitch(images_data)

        # Stitched successfully
        if status == 0:

            # Perform additional cropping
            if self.cb_mode.currentText() == "Default Cropped":

                # Create a 10-pixel border surrounding the stitched image
                stitched = copyMakeBorder(stitched, 10, 10, 10, 10, BORDER_CONSTANT, (0, 0, 0))

                # Convert the stitched image to grayscale and threshold it
                # Pixels greater than zero are set to 255 and all others remain 0
                stitched_gray = cvtColor(stitched.copy(), COLOR_BGR2GRAY)
                stitched_thresh = threshold(stitched_gray, 0, 255, THRESH_BINARY)[1]

                # Find external contours in the threshold image, then find the contour
                # with the largest area, which is an outline of the stitched image
                contours = findContours(stitched_thresh.copy(), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
                contours = grab_contours(contours)
                outline = max(contours, key=contourArea)

                # Allocate memory for the new mask, then
                # calculate the bounding box of the largest contour, and
                # using this box, draw a solid white rectangle on the mask
                mask = zeros(stitched_thresh.shape, dtype="uint8")
                x, y, w, h = boundingRect(outline)
                rectangle(mask, (x, y), (x + w, y + h), 255, -1)

                # Create two copies of the mask:
                # the first mask will be slowly reduced in size
                # until it can fit inside the inner part of the panorama;
                # the second mask will be used to determine
                # if we need to keep reducing the size of the first mask
                crop = mask.copy()
                sub = mask.copy()

                # Loop until there are no non-zero pixels left in the subtracted image.
                # By the end of the loop, we will calculate the smallest rectangular mask
                # that can fit into the largest rectangular region of the panorama
                while countNonZero(sub) > 0:
                    # Erode the minimum rectangular mask and then
                    # subtract the thresholded image from the minimum rectangular mask
                    crop = erode(crop, None)
                    sub = subtract(crop, stitched_thresh)

                # Find the contours of the minimum rectangular mask, then
                # extract the bounding box coordinates
                contours = findContours(crop.copy(), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
                contours = grab_contours(contours)
                contour = max(contours, key=contourArea)
                x, y, w, h = boundingRect(contour)

                # Use the bounding box coordinates to extract the final stitched image (ROI)
                stitched = stitched[y:y + h, x:x + w].copy()

        return status, stitched

    def stitch_images(self):
        """
        Stitch selected images to the panorama.

        There are three stitch modes:
            - Default: use builtin OpenCV .stitch() method.
            - Default Cropped: same as previous, but with smart cropping to cut out black borders
            - Manual: own implementation; see :method:`stitch_manually` for more information.

        Noticed that the default built-in OpenCV mode has some problems with stitching the same images several times.
        If you try to stitch the same photos several times, sometimes you will get a little bit different output,
        which can cause program errors.
        """

        images_data = self.get_selected_images()

        if self.cb_mode.currentText() == "Manual":
            status, stitched = self.stitch_manually(images_data)
        else:
            try:
                status, stitched = self.stitch_built_in(images_data)
            except ValueError:
                self.label_errors.setText("Calculation Error. Restart the application and try again.")
                return
            except Exception:
                self.label_errors.setText("Unexpected error happened. Restart the application and try again.")
                return

        if status == 0:
            self.pano_data = stitched
            self.pano_name = self.edit_pano_name.text().strip()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", self.ERROR_MESSAGES[status])
