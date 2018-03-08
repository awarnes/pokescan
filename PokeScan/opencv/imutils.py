"""
Base functions for manipulating images with OpenCV.
"""

import numpy as np
import cv2

def resize(image, height=100.0):
    """
    Given an image path, returns a resized image with proper aspect ratio.
    Defaults:
      height = 100 px
    """
    ratio = height / image.shape[0]
    dim = (int(image.shape[1] * ratio), int(height))
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    return resized

def rotate_around(image, angle=180):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def crop(image, y1, y2, x1, x2):
    """
    Given an image path returns a cropped image.
    Defaults:
      color = 0 (Greyscale)
    """
    cropped = image[y1:y2, x1:x2]

    return cropped

def display(images, title = "Image"):
    """
    Displays an image in window and waits before closing.
    Defaults:
      title = "Image"
    """
    for image in images:
        cv2.imshow(title, image)

    cv2.waitKey(0)
    cv2.destroyWindow(title)

def is_cv2():
    return check_opencv_version("2.")

def is_cv3():
    return check_opencv_version("3.")

def check_opencv_version(major, lib=None):
    if lib is None:
            import cv2 as lib
    return lib.__version__.startswith(major)