import imutils
import cv2
image_path = "/Users/alexanderwarnes/Downloads/IMG-0526.JPG"
image = cv2.imread(image_path)
imutils.display(imutils.resize(imutils.resize(image, 10), 500))
