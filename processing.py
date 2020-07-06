import numpy as np
import cv2 as cv

kernel = np.ones((5, 5), np.uint8)
orange = (11, 159, 255, 255)
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
crimson = (93, 11, 217, 255)

def getMask(mask, markers=None ,flag=None):
    if flag == None:
        transp_mask = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
        transp_mask = cv.morphologyEx(transp_mask, cv.MORPH_OPEN, kernel)
    elif flag == 'y':
        mask[markers == 0] = 0
        mask[markers == 255] = 255
        transp_mask = mask

    return transp_mask


def remoweBg(img, mask):
    bgra_img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    bgra_img = cv.bitwise_and(bgra_img, bgra_img, mask=mask)

    return bgra_img


def showContour(img, mask, color=crimson, flag='show'):
    img = img.copy()
    mask = cv.dilate(mask, np.ones((2, 2), np.uint8))
    mask = cv.medianBlur(mask, 7)
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img, contours, -1, color, 2, cv.LINE_AA, _, 2)

    if flag == 'draw':
        d_mask = cv.dilate(mask, np.ones((17, 17), np.uint8))
        blur = cv.medianBlur(d_mask, 11)
        contour = cv.subtract(blur, mask)
        img[contour>0] = white

    return img


def smoothing(img):
    blur = cv.bilateralFilter(img[:, :, :3], 15, 30, 30)
    img[:, :, :3] = blur

    return img

