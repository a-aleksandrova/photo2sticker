from processing import*
from test_rect import*
from test_paint import*
from minor_features import*
import cv2 as cv
import numpy as np

filename = 'ada6.jpg'

img = getPngImg(filename)
img = setNormSize(img)

sf_img = nparray2surfase(img)
rectangle = get_rects(sf_img)

mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
cv.grabCut(img, mask, rectangle, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)

first_fg_mask = getMask(mask)
img_with_contour = showContour(img, first_fg_mask)

feedback = getFeedback(img_with_contour, 'Do you want to edit the borders?[y/n]')
manual_mode = None
while feedback == 'y':
    sf_img_with_contour = nparray2surfase(img_with_contour)
    print('Orange for fg\nBlue for bg\nChange color alt+l')
    sf_markers = getMarker(sf_img_with_contour) #run paint
    bgr_markers = surface2nparray(sf_markers)
    markers = bgr_markers[:,:,2] #get red channel

    if manual_mode == None:
        mask[markers == 0] = 0
        mask[markers == 255] = 1
        mask, bgdModel, fgdModel = cv.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_MASK)
        fg_mask = mask

    fg_mask = getMask(fg_mask, markers=markers, flag=manual_mode)
    img_with_contour = showContour(img, fg_mask)

    manual_mode = getFeedback(img_with_contour, 'Does the border still need to be changed?[y/n]')
    feedback = manual_mode


result = remoweBg(img, fg_mask)

contour_feedback = getFeedback(result, 'Add contour?[y/n]')
if contour_feedback == 'y':
    result = showContour(result, fg_mask, color=(200, 213, 48, 255))

finish_feedback = getFeedback(result, 'Save the result?[y/n]')
if finish_feedback == 'y':
    print('Input name:')
    name = input()
    cv.imwrite('{}.png'.format(name), result)
    print('Result saved as {}.png'.format(name))

elif finish_feedback == 'n':
    print('Result not saved')