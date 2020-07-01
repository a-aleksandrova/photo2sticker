import numpy as np
import cv2 as cv

kernel = np.ones((5,5), np.uint8)

def getMask(mask):
    transp_mask = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
    transp_mask = cv.morphologyEx(transp_mask, cv.MORPH_OPEN, kernel)

    return transp_mask


def remoweBg(img, mask):
    bgra_img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    bgra_img = cv.bitwise_and(bgra_img, bgra_img, mask=mask)

    return bgra_img


def showContour(img, mask, color=(11, 159, 255, 255)):
    img = img.copy()
    contours, _ = cv.findContours(cv.dilate(mask, np.ones((3,3), np.uint8)), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img, contours, -1, color, 2, cv.LINE_4, _, 1)

    return img
