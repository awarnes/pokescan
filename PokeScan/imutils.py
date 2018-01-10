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

def rotateImageAroundCenter(image, degrees = 180):
    """
    Given an image patth returns an image rotated x degrees around center.
    Defaults:
      degrees = 180
      color = 0 (Greyscale)
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    matrix = cv2.getRotationMatrix2D(center, degrees, 1.0) # point, degrees, ratio change
    rotated = cv2.warpAffine(image, matrix, (w, h))

    return rotated

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