import numpy as np
import cv2 as cv
import time

start = time.time()

def getPngImg(filename):
    format = filename.split('.')[-1]
    origin_img = cv.imread(filename)

    # позднее заменить на if format in [список форматов поддерживающих альфа-канал]
    if format == 'png':
        print('Получен файл в формате .png')
        return origin_img

    # позднее заменить на elif format in [список форматов не поддерживающих альфа-канал]
    # и добавить обработку исключений
    else:
        _, buf_img = cv.imencode('.png', origin_img)
        converted_img = cv.imdecode(buf_img, -1)
        print('Получен файл в формате .{}'.format(format))
        print('Файл переведен в формат .png')
        return converted_img

def getMaskByRect(img):
    cv.grabCut(img, mask, rectangle, bgModel, fgModel, 5, cv.GC_INIT_WITH_RECT)
    transp_mask = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
    transp_mask = cv.morphologyEx(transp_mask, cv.MORPH_OPEN, kernel)
    print('Определена первая маска')

    return transp_mask

def makeBgTransparent(img, mask):
    img = img.copy()
    img[..., 3] = mask
    print('Удален фон')

    return img

def smoothEdges(img, mask):
    edges = cv.morphologyEx(mask, cv.MORPH_GRADIENT, kernel)
    bl = cv.GaussianBlur(img, (5, 5), 0)
    img[edges > 0] = bl[edges > 0]
    print('Сглажены края')
    return img

def drawContour(img, mask):
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img, contours, -1, (255, 159, 11, 255), 2, cv.LINE_4, _, 1)
    print('Отрисован контур')

    return img

#второе тестовое изображение
#filename = 'yana.jpg'
#rectangle = (10, 9, 633, 853)

filename = 'ada.png'
rectangle =(0, 20, 359, 539)
#в дальнейшем координаты будут загружаться по отрисованному пользователем прямоугольнику

png_img = getPngImg(filename)

mask = np.zeros(png_img.shape[:2], np.uint8)
bgModel = np.zeros((1, 65), np.float64)
fgModel = np.zeros((1, 65), np.float64)
kernel = np.ones((5,5), np.uint8)

bgra_img = cv.cvtColor(png_img, cv.COLOR_BGR2BGRA) #стоить перенести в getPngImg()?
fg_mask = getMaskByRect(png_img)
img_with_contour = drawContour(png_img, fg_mask)

fg_img = makeBgTransparent(bgra_img, fg_mask)
smooth_edges = smoothEdges(fg_img, fg_mask)

cv.imshow('countor', img_with_contour)
cv.imwrite('first_res.png', smooth_edges) # в opencv не видна прозрачность при imshow

print('{} seconds'.format(time.time() - start))

cv.waitKey()