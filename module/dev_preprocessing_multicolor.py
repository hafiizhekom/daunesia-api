import cv2
import numpy as np
from os import walk
import os
sensitivity = 20
gauss_win_size = 5
gauss_sigma = 3
th_window_size = 15
th_offset = 2

def brigtning(img):
    height, width = img.shape[:2]
    image = img

    new_image = np.zeros(image.shape, image.dtype)

    alpha = 1.0  # Simple contrast control
    beta = 0  # Simple brightness control

    try:
        alpha = float(1.5)
        beta = int(50)
    except ValueError:
        print('Error, not a number')

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y, x, c] = np.clip(alpha * image[y, x, c] + beta, 0, 255)

    return new_image


def crop_rotate(img):
    height, width = img.shape[:2]
    img = cv2.resize(img, (int(width / 10), int(height / 10)), interpolation=cv2.INTER_CUBIC)
    if (height < width) and (height != width):
       dst = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    else:
        dst = img
    crop_img = dst[55:355, 0:300]
    return crop_img

def get_biggest_scracth(img):
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img)

    sizes = stats[1:, -1];
    if len(sizes) < 1:
        return img
    else:
        nb_components = nb_components - 1
        min_size = max(sizes) - 1

        img2 = np.zeros((output.shape))
        for i in range(0, nb_components):
            if sizes[i] >= min_size:
                img2[output == i + 1] = 255

        return img2

def closingHoleContour(img):
    dilate = cv2.bitwise_not(img)
    im2, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    reclear = dilate
    for holes in range(0, len(contours) - 2):
        reclear = cv2.drawContours(reclear, contours, holes, (0, 255, 0), 1)
    dilate = cv2.bitwise_not(reclear)

    return dilate

def binarize_multicolor(img):
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    dst = cv2.fastNlMeansDenoisingColored(dst, None, 10, 10, 7, 21)
    dst = cv2.GaussianBlur(img, (gauss_win_size, gauss_win_size), gauss_sigma)

    # Take each frame
    frame = dst

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of yellow color in HSV
    lower_blue = np.array([25 - sensitivity, 30, 10])
    upper_blue = np.array([60 + sensitivity, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('res', res)

    kernel_closing = np.ones((2, 2), np.uint8)
    kernel_opening = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_closing)
    # opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel_opening)
    # dilate = cv2.dilate(opening,kernel_closing,iterations=1)
    # dilate = cv2.dilate(dilate,kernel_closing,iterations=1)
    # dilate

    # cv2.imwrite("example2_binarize.jpg", dilate)

    # cv2.imshow('dilate',dilate)

    # cv2.waitKey(0)

    # test = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    #dilate = cv2.bitwise_not(closing)
    #im2, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #reclear = dilate
    #for holes in range(0, len(contours) - 2):
    #    reclear = cv2.drawContours(reclear, contours, holes, (0, 255, 0), 1)

    #dilate = cv2.bitwise_not(reclear)

    return closing

def replaceWhite(img,new_img):
    height, width = img.shape[:2]

    blank = np.zeros([height, width, 3], dtype=np.uint8)
    blank.fill(0)  # or img[:] = 255

    for x in range(0, width):
        for y in range(0, height):
            if (img[y, x] >= 200) and (img[y, x] <= 255):
                #print img[y, x]
                blank[y, x] = new_img[y, x]
            else:
                a = 0
                # print "hitam"

    return blank

def preprocessing(id_predict, typeimage):

    #mypath = "/home/hafiizhekom/Documents/Dataset Daun/Alang Alang"
    #destinationpath = "/home/hafiizhekom/Documents/Dataset Daun/result_dracaena"

    path = "./data/temporary/predict_image"
    mypath = path
    destinationpath = path

    print("Mempersiapkan gambar untuk dilakukan preprocessing multicolor")
    img = cv2.imread(mypath+"/"+id_predict+"/"+id_predict+"."+typeimage, cv2.IMREAD_COLOR)

    print("Mulai #Multicolor Preprocessing")
    img = crop_rotate(img)
    imgcolor = brigtning(img)
    img = binarize_multicolor(img)
    img = get_biggest_scracth(img)
    img = replaceWhite(img, imgcolor)
    print("Menyimpan hasil preprocessing multicolor")
    cv2.imwrite(destinationpath+"/"+id_predict+"/"+id_predict+"-multicolor." + typeimage,img)

    print("Selesai #Multicolor Preprocessing")
    return True

