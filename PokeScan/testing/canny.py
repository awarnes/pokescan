import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('/Users/alexanderwarnes/Desktop/PokeScan-Photos/originals/FourthBatch/1TestScans/IMG_1903.jpg', 0)
sigma = 0.33
v = np.median(img)
 
# apply automatic Canny edge detection using the computed median
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
edges = cv2.Canny(img, lower, upper)
cnts = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

for (i, c) in enumerate(cnts[1]):
  cv2.drawContours(img, [c], -1, (0, 255, 0), 3)

plt.subplot(121)
plt.imshow(img)
plt.title('Original Image')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(edges, cmap = 'gray')
plt.title('Edge Image')
plt.xticks([])
plt.yticks([])

plt.show()