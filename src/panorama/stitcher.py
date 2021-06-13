from cv2 import (ORB_create, BFMatcher_create, perspectiveTransform, warpPerspective, findHomography,
                 NORM_HAMMING, RANSAC, drawKeypoints, imshow, waitKey)
from numpy import array, concatenate, float32, int32


class Stitcher:
    """
    The Stitcher class implements manual stitching between two images.

    Panorama (stitch) algorithm:
        - Detect keypoints and descriptors.
        - Detect a set of matching points that is present in both images (overlapping area).
        - Apply the RANSAC method to improve the matching process detection.
        - Apply perspective transformation on the first image using the second image as a reference frame.
        - Stitch images together.
    """

    # Minimum match condition
    MIN_MATCH_COUNT = 10

    # The maximum pixel "wiggle room" allowed by the RANSAC algorithm
    REPROJ_THRESH = 5.0

    def __init__(self, images, nfeatures, details=False):
        """
        Create a new Stitcher instance.

        :param images: The two images to stitch
        :type images: list
        :param nfeatures: The maximum number of features to be detected in each image
        :type nfeatures: int
        :param details: The flag to indicate whether show keypoints or not
        :type details: bool
        """

        assert len(images) == 2, AttributeError("Can stitch only two images")

        self.images = images
        self.nfeatures = nfeatures
        self.details = details
        self.keypoints = []
        self.descriptors = []
        self.good_matches = []

    def detect_keypoints(self):
        """Detect keypoints and descriptors."""

        # Create an ORB detector to extract the keypoints
        orb = ORB_create(nfeatures=self.nfeatures)

        # Find the keypoints and descriptors using ORB
        keypoints1, descriptors1 = orb.detectAndCompute(self.images[0], None)
        keypoints2, descriptors2 = orb.detectAndCompute(self.images[1], None)
        self.keypoints.extend([keypoints1, keypoints2])
        self.descriptors.extend([descriptors1, descriptors2])

        # Draw all keypoints for images
        if self.details:
            imshow("Image 1: All Keypoints", drawKeypoints(self.images[0], keypoints1, None, (255, 0, 255)))
            imshow("Image 2: All Keypoints", drawKeypoints(self.images[1], keypoints2, None, (255, 0, 255)))
            waitKey(0)

    def match_keypoints(self):
        """Match keypoints (features) between two images."""

        # Create a BFMMatcher object to find all the matching keypoints
        bf = BFMatcher_create(NORM_HAMMING)

        # Find matching features
        matches = bf.knnMatch(self.descriptors[0], self.descriptors[1], k=2)

        # Keep only strong matches
        for m, n in matches:
            if m.distance < 0.6 * n.distance:
                self.good_matches.append(m)

        # Draw only matching strong keypoints for images
        if self.details:
            matched_keypoints1 = [self.keypoints[0][m.queryIdx] for m in self.good_matches]
            matched_keypoints2 = [self.keypoints[1][m.trainIdx] for m in self.good_matches]

            imshow("Image 1: Matched Strong Keypoints",
                   drawKeypoints(self.images[0], matched_keypoints1, None, (255, 0, 255)))
            imshow("Image 2: Matched Strong Keypoints",
                   drawKeypoints(self.images[1], matched_keypoints2, None, (255, 0, 255)))

            waitKey(0)

    @staticmethod
    def warp_images(image1, image2, H):
        """
        Warp perspective for the first image and stitch it with the referenced second image.

        :param image1: The first image to warp perspective
        :type image1: `numpy.ndarray`
        :param image2: The second image as the reference
        :type image2: `numpy.ndarray`
        :param H: The homography 3x3 matrix
        :type H: `numpy.ndarray`
        :return: The stitched image
        :rtype: `numpy.ndarray`
        """

        rows1, cols1 = image1.shape[:2]
        rows2, cols2 = image2.shape[:2]

        # Coordinates of the image to transform
        temp_points1 = float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)

        # Coordinates of a reference image
        points2 = float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1, 1, 2)
        points1 = perspectiveTransform(temp_points1, H)
        points = concatenate((points2, points1), axis=0)

        [x_min, y_min] = int32(points.min(axis=0).ravel() - 0.5)
        [x_max, y_max] = int32(points.max(axis=0).ravel() + 0.5)

        translation_dist = [-x_min, -y_min]
        H_translation = array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

        output_img = warpPerspective(image1, H_translation.dot(H), (x_max - x_min, y_max - y_min))
        output_img[translation_dist[1]:rows2 + translation_dist[1],
                   translation_dist[0]:cols2 + translation_dist[0]] = image2

        return output_img

    def stitch(self):
        """
        Perform all the stitching algorithm.

        - Detect keypoints using :method:`detect_keypoints`.
        - Match keypoints using :method:`match_keypoints`.
        - Make sure we found at least the minimum number of matches defined in :attr:`MIN_MATCH_COUNT`.
        - Calculate homography 3x3 matrix using RANSAC procedure.
        - Stitch images using :method:`warp_images`.
        """

        self.detect_keypoints()
        self.match_keypoints()

        if len(self.good_matches) > self.MIN_MATCH_COUNT:

            # Convert keypoints to an argument for findHomography
            src_points = float32([self.keypoints[0][m.queryIdx].pt for m in self.good_matches]).reshape(-1, 1, 2)
            dst_points = float32([self.keypoints[1][m.trainIdx].pt for m in self.good_matches]).reshape(-1, 1, 2)

            # Establish a homography
            M, _ = findHomography(src_points, dst_points, RANSAC, self.REPROJ_THRESH)

            result = self.warp_images(*self.images, M)
            return 0, result

        # Error: not found enough strong matches between images
        return 1, None
