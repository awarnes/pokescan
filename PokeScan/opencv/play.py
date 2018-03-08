import numpy as np
import cv2

image_path = "/Users/alexanderwarnes/Downloads/IMG-0526.JPG"
# Load a color image in greyscale
image = cv2.imread(image_path, 0)

# Resize image with proper aspect ratio
ratio = 500.0 / image.shape[1]
dim = (500, int(image.shape[0] * ratio))
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

# Rotate image 180 degrees around center
(h, w) = image.shape[:2]
center = (w / 2, h / 2)
matrix = cv2.getRotationMatrix2D(center, 180, 1.0) # point, degrees, ratio change
rotated = cv2.warpAffine(image, matrix, (w, h))

# Crop image (y, x)
cropped = image[60:215, 75:200]

cv2.imshow('cropped', cropped)
cv2.imshow('rotated', rotated)
cv2.imshow('original', image)
cv2.imshow('resized', resized)
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()