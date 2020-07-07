import cv2 as cv
from test_rect import*


def setNormSize(img, norm=512):
    x, y = img.shape[:2]
    if x > y:
        x1 = norm
        y1 = int(y // (x / norm))
    else:
        y1 = norm
        x1 = int(x // (y / norm))

    resized_img = cv.resize(img, (y1, x1))

    return resized_img

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


def cropImgMask(img, mask):
    sf_img = nparray2surfase(img)
    rectangle = get_rects(sf_img)
    x, y, x1, y1 = rectangle
    img = img[y:y1, x:x1]
    mask = mask[y:y1, x:x1]

    return img, mask