"""
Applies scan.py to an entire folder
and writes new files to another folder.
"""
from scan import scan
import imutils
import cv2
import argparse
import os

IMAGE_EXT = ".jpg"

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", required=True,
  help="path to folder with images to scan")
ap.add_argument("-o", "--output", required=False,
  help="path to output folder")

args = vars(ap.parse_args())
inputPath = args["input"]
outputPath = args["output"] if args["output"] else "~/Desktop"

if os.path.isfile(args["input"]):
    print("You gave just a single image, not saving...")
    original = cv2.imread(args["input"])
    fixed = scan(original)
    fixed = imutils.resize(fixed, 500)
    imutils.display([original, fixed])
else:
    images = [(os.path.join(inputPath, fileName), fileName) for fileName in os.listdir(inputPath) if fileName.endswith(IMAGE_EXT)]

    for image, fileName in images:
        original = cv2.imread(image)
        print(image)
        scanned = scan(original)
        cv2.imwrite(os.path.join(outputPath, fileName), scanned)
