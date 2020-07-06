from math import sqrt
import cv2 as cv
import pygame as pg

def setNormSize(img):
    norm = 160000
    x, y = img.shape[0:2]
    k = sqrt((x * y) / norm)
    x, y = int(x // k), int(y // k)
    resize_img = cv.resize(img, (y, x))

    return resize_img

def getPngImg(filename):
    format = filename.split('.')[-1]
    img = cv.imread(filename)
    if format == 'png':
        print('File loaded as .png')

    else:
        _, buf_img = cv.imencode('.png', img)
        img = cv.imdecode(buf_img, -1)
        print('File received as .{}'.format(format))
        print('File converted to .png')

    return img


def nparray2surfase(img):
    rgb = img[:,:,(2,1,0)]
    roteted = rgb.swapaxes(0, 1) #set the correct h,w
    surfase = pg.surfarray.make_surface(roteted)

    return surfase


def surface2nparray(img):
    np_img = pg.surfarray.array3d(img)
    rotated = np_img.swapaxes(0, 1)#set the correct h,w
    bgr = rotated[:, :, (2, 1, 0)]

    return bgr

def getFeedback(img, text):
    cv.imshow('img', img)
    print(text)
    answer = chr(cv.waitKey() & 0xff)
    while answer not in ['y', 'n']:
        print('Press y or n')
        answer = chr(cv.waitKey() & 0xff)

    cv.destroyWindow('img')

    return answer

def cropToSquare(img, rectangle):
    x, y, x1, y1 = rectangle
    img = img[y:y1, x:x1]

    rows, cols = img.shape[0:2]
    x = max(rows, cols)
    if x == rows:
        indent_c = (rows - cols) // 2 + 22
        indent_r = (rows - cols) % 2 + 22
    else:
        indent_r = (cols - rows) // 2 + 22
        indent_c = (rows - cols) % 2 + 22

    res = cv.copyMakeBorder(img, indent_r, indent_r, indent_c, indent_c, cv.BORDER_CONSTANT)

    return res