import numpy as np
import cv2

def orderPoints(pts):
    """
    Initialize a list of coords that will be ordered,
    such that the first entry in the list is the top-left,
    second is top-right, third is bottom-right, and fourth
    is bottom-left.
    """

    rect = np.zeros((4, 2), dtype = "float32")

    # top-left with have the smallest sum,
    # bottom right will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def fourPointTransform(image, pts):
    rect = orderPoints(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Compute 'destination' points:
    dest = np.array([
      [0, 0],
      [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1],
      [0, maxHeight - 1]], dtype = "float32")
    
    # Compute the perspective transform matrix and apply it:
    M = cv2.getPerspectiveTransform(rect, dest)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped