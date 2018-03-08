from transform import fourPointTransform
import imutils
import numpy as np
import cv2

def scan(image):
    """
    Returns a 'birds-eye-view' of an input image allowing for
    normalization of input images for OCR.
    """
    ratio = image.shape[0] / 1000.0
    orig = image.copy()
    image = imutils.resize(image, height = 1000)

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (5, 5), 0)
    edged = cv2.Canny(grey, 75, 200)

    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break
    try:
        warped = fourPointTransform(orig, screenCnt.reshape(4, 2) * ratio)
        return warped
    except:
        print("contours not found on this image...")
        return False
