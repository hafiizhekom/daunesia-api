import cv2
import numpy as np

def extract_yellow_contour(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = 30
    v = 255
    lower = np.array([h - 10, 40, v - 40])
    upper = np.array([h + 10, 255, v + 40])
    image_mask = cv2.inRange(img, lower, upper)

    # CLOSING
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(image_mask, cv2.MORPH_CLOSE, kernel)

    # BINARIZE
    ret, thresh1 = cv2.threshold(closing, 127, 255, cv2.THRESH_BINARY)

    # FIND CONTOURS
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(thresh1, contours, -1, (50, 150, 150), 4)

    listarea = []
    if (len(contours) > 0):
        for index, val in enumerate(contours):
            listarea.append(cv2.contourArea(contours[index]))
        return max(listarea)
    else:
        return 0

def compare_result(id_predict, type_image):
    mypath = './data/temporary/predict_image'
    img_binarize = cv2.imread(mypath + "/" + id_predict + "/" + id_predict + "-binarize." + type_image)
    img_multicolor = cv2.imread(mypath + "/" + id_predict + "/" + id_predict + "-multicolor." + type_image)
    multicolor_value=extract_yellow_contour(img_multicolor)
    binarize_value = extract_yellow_contour(img_binarize)
    print("multicolor: ",multicolor_value)
    print("binarize: ", binarize_value)
    if ( binarize_value < 24) and ( multicolor_value < 24):
        return "binarize"
    elif multicolor_value > 24:
        return "multicolor"
    elif binarize_value > 24:
        return "multicolor"
    else:
        return "binarize"

