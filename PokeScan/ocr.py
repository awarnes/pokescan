"""
The OCR center of PokeScan
"""

import argparse
import time

import constants
import tesseract.tesseract_methods as tm
from opencv.imutils import rotate_around
import os

"""
At some point will need to see about ocr-ing just the corners
of each card to speed up process.
"""

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--image", metavar="path", default=os.getcwd(),
    help="path to input image")
ap.add_argument("-r", "--dir", action="store_true", default=True,
    help="if provided will OCR all images in given path")
ap.add_argument("--reference", metavar="ref",
    help="path to reference OCR image")
ap.add_argument("-v", "--version", action="version", version="0.0.1")
args = vars(ap.parse_args())

inputImage = args["image"]
referenceImage = args["reference"]
directory = args["dir"]

def main():
    images = list(inputImage)
    total = 0
    if dir:
        try:
            images = [os.path.join(inputImage, photo) for _, _, photos in os.walk(inputImage) for photo in photos if os.path.basename(photo).split('.')[1] in ['jpg', 'png', 'jpeg']]
        except IndexError:
            print('Wrong Folder!')
            return
        print(f'Total Length: {len(images)}')
        for image in images:
            img = tm.get_image(image)
            if tm.verify_and_parse_result(tm.ocr_image(tm.get_part_of_image(img))):

                # print(tm.verify_and_parse_result(tm.ocr_image(tm.get_part_of_image(img))))
                total = total + 1
                print(f'{total} / {len(images)}')
            # else:
            #     # print(tm.verify_and_parse_result(tm.ocr_image(tm.get_part_of_image(rotate_around(img)))))
    
    print(f'Completed Total: {total}')
    print(f'Percent Read: {total / len(images)}')

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()

    print(end - start)
