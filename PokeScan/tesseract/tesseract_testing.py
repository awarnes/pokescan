import numpy as np
import argparse
import cv2
import pytesseract
import re
from imutils import rotate_bound 

# imagePath = "/Users/alexanderwarnes/Desktop/PokeScan-Photos/originals/FifthBatch/FixedCards/IMG_2101.jpg"

imagePath = "/Users/alexanderwarnes/Desktop/PokeScan-Photos/originals/FourthBatch/1TestScans/IMG_1882.jpg"

img = cv2.imread(imagePath)
height, _, _ = img.shape
print(height)

bottom10 = height - int(height * .12)
# get image height, get bottom 10% and crop to that height

result = pytesseract.image_to_string(img[bottom10:height,:])
print(result)

check_pattern = re.compile(r'Illus.')

if len(re.findall(check_pattern, result)) == 0:
    print('wrong way up, recallibrating')
    rotated = rotate_bound(img, 180)
    print('recalibrated, ocr-ing now')
    result = pytesseract.image_to_string(rotated[bottom10:height,:])

print(f'new result \n {result}')
number_pattern = re.compile(r'\d{1,3}/\d{1,3}')

print(re.findall(number_pattern, result)[0].split('/'))


