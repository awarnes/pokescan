import imutils
import contours
import numpy as np
import argparse
import cv2
import os

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#     help="path to input image")
# ap.add_argument("-r", "--reference", required=True,
#     help="path to reference OCR image")
# args = vars(ap.parse_args())

# inputImage = args["image"]
# referenceImage = args["reference"]

def ocrSetNumber(inputImage):
    referenceImage = "/Users/alexanderwarnes/Desktop/PokeScan-Photos/CardFakingResources/PokemonNumbers/Gill-Std-Condensed.jpg"


    # Get reference images to compare to
    ref = cv2.imread(referenceImage)
    # cv2.imshow('fuck you cunt', ref)
    # cv2.waitKey(0)
    ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
    refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
    refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
    digits = dict()
    for (i, c) in enumerate(refCnts):
        (x, y, w, h) = cv2.boundingRect(c)
        roi = ref[y-1:y+h + 1, x-1:x+w + 1] if i == 0 else ref[y:y+h, x:x+w]
        roi = cv2.resize(roi, (57, 88))
        if (i == 9): i = -1
        digits[i + 1] = roi

    # for (index, image) in digits.items():
    #     cv2.imshow(f"number{index}", image)

    # Set up image to compare to.
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 10))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    # print(inputImage)
    image = cv2.imread(inputImage)
    # cv2.namedWindow("first", cv2.WINDOW_NORMAL)
    # cv2.imshow("first", image)
    # image = imutils.resize(image, 1000)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    blackhat = cv2.morphologyEx(blurred, cv2.MORPH_BLACKHAT, rectKernel)

    gradX = cv2.Sobel(blackhat, cv2.CV_64F, dx=1, dy=0, ksize=-1)

    # cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
    # cv2.imshow('thresh', gradX)
    # cv2.waitKey(0)

    gradX = np.absolute(gradX)

    (minVal, maxVal) = (np.min(gradX), np.max(gradX))

    gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))

    gradX = gradX.astype("uint8")

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)

    thresh = cv2.threshold(gradX, 0, 255,
        cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]



    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    locs = list()
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        # cv2.drawContours(original, [c], -1, (0, 0, 255), 1)
        # 2900, 3250, 1900, 2250
        if (1900 < x < 2250 and 2900 < y < 3250) or (100 < x < 500 and 2900 < y < 3250):
            # if 3.0 < ar < 7.0:
            if (90 < w < 220) and (10 < h < 45):
                # cv2.drawContours(original, [c], -1, (0, 255, 0), 1)
                locs.append((x, y, w, h))

    locs = sorted(locs, key=lambda x:x[0])
    output = list()
    # print(locs)
    for (i, (gX, gY, gW, gH)) in enumerate(locs):
        groupOutput = list()

        group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
        
        group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # cv2.imshow('group', group)
        digitCnts = cv2.findContours(group.copy(), cv2.RETR_CCOMP,
            cv2.CHAIN_APPROX_NONE)
        digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
        digitCnts = contours.sort_contours(digitCnts)[0]
        digitCnts = [cnt for cnt in digitCnts[1:] if cv2.contourArea(cnt) > 75]
        # cv2.drawContours(original, digitCnts, -1, (0, 0, 255), 1)
        # cv2.imshow('cnts', original)
        for (i, c) in enumerate(digitCnts):
            (x, y, w, h) = cv2.boundingRect(c)
            roi = group[y: y + h, x: x+ w]
            roi = cv2.resize(roi, (57, 88))
            scores = list()

            for (digit, digitROI) in digits.items():
                result = cv2.matchTemplate(cv2.bitwise_not(roi), digitROI, cv2.TM_CCOEFF_NORMED)
                (_, score, _, _) = cv2.minMaxLoc(result)
                scores.append(score)

            
            ocrNumber = np.argmax(scores) + 1
            ocrNumber = ocrNumber if ocrNumber < 10 else 0 
            groupOutput.append(str(ocrNumber))
            # cv2.imshow(f'roi{i}', np.hstack((cv2.bitwise_not(roi), digits[ocrNumber])))
            # cv2.imshow(f'roi{i}', np.hstack((cv2.bitwise_not(roi), digits[8])))
            # print(ocrNumber)

        cv2.rectangle(original, (gX - 10, gY - 10),
            (gX + gW + 10, gY + gH + 10), (0, 0, 255), 2)
        cv2.putText(original, "".join(groupOutput), (gX, gY - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
        ocrdNumber = imutils.crop(original, 2900, 3250, 100, 500)
        # ocrdNumber = cv2.cvtColor(ocrdNumber, cv2.COLOR_BGR2GRAY)
        output.extend(groupOutput)
        print("success")
        return "".join(output), ocrdNumber

    base = os.path.basename(os.path.normpath(inputImage))
    print(f"failed {base}")
    ocrdNumber = imutils.crop(original, 2900, 3250, 100, 500)
    # ocrdNumber = cv2.cvtColor(ocrdNumber, cv2.COLOR_BGR2GRAY)
    return base, ocrdNumber

IMAGE_EXT = ".jpg"

dirPath = "/Users/alexanderwarnes/Desktop/PokeScan-Photos/originals/FifthBatch/FixedCards"
outputPath = "/Users/alexanderwarnes/Desktop/PokeScan-Photos/originals/FifthBatch/OCRCards"

images = [os.path.join(dirPath, fileName) for fileName in os.listdir(dirPath) if fileName.endswith(IMAGE_EXT)]

for image in images:
    # original = cv2.imread(image)
    outputNumber, outputPhoto = ocrSetNumber(image)
    ending = "" if outputNumber.endswith(IMAGE_EXT) else IMAGE_EXT
    cv2.imwrite(os.path.join(outputPath, f"{outputNumber}{ending}"), outputPhoto)

# fileName = "".join(ocrSetNumber(dirPath))
# ocrdNumber = imutils.crop(original, 2900, 3250, 1900, 2250)
# ocrdNumber = cv2.cvtColor(ocrdNumber, cv2.COLOR_BGR2GRAY)
# print(ocrdNumber)
# cv2.imshow('play', ocrdNumber)

# cv2.imwrite(outputPath, ocrdNumber)



# cv2.imshow("thresh", thresh)
# cv2.imshow("gradX", gradX)
# cv2.imshow("tophat", tophat)

# print(f"number: {''.join(output)}")
# cv2.namedWindow("original", cv2.WINDOW_NORMAL)
# cv2.imshow("original", original)
# cv2.waitKey(0)
# cv2.destroyAllWindows()