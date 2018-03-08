import re, math
import argparse

import numpy as np
import pytesseract, cv2

from opencv.imutils import rotate_around
from helpers import logger
import constants


def get_image(path, color=constants.BLACK_AND_WHITE):
    "Returns a cv2 image from path in black and white"
    return cv2.imread(path)

def get_part_of_image(image, search_area=.12):
    "Returns a percentage of the image (vertically)."
    height, _, _ = image.shape
    bottom = height - (height * search_area)
    return image[math.floor(bottom):height,:]

def ocr_image(image):
    """
    Runs tesseract on image for text.
    @returns OCR'd text
    """

    return pytesseract.image_to_string(image)

def check_correct_orientation(info, verbose=False):
    """
    Verifies the card is right-side-up.
    @returns True if right-side-up
    @returns False if wrong-side-up
    """

    logger(info, verbose)

    check_pattern = re.compile(constants.CHECK_ORIENTATION_PATTERN)
    print(re.findall(constants.CHECK_ORIENTATION_PATTERN, info))
    if len(re.findall(constants.CHECK_ORIENTATION_PATTERN, info)) == 0:
        logger('Wrong way up', verbose)
        return False

    logger('Right way up!', verbose)
    return True

def verify_and_parse_result(info):
    """
    Returns the parsed data.
    @returns list - [0] = card number, [1] = total cards in set
    """

    try:
        return re.findall(constants.NUMBER_PATTERN, info)[0].split('/')
    except IndexError:
        pass
        # return "Couldn't get anything out of this:\n {}".format(info)