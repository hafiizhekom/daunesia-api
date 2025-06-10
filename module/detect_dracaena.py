import cv2
import numpy as np
from os import walk
import os
from tqdm import tqdm

path = "/home/hafiizhekom/Documents/Dataset Daun/CITS Color"

filenames_plant = []

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
listcontourleaf = []

for (dirpath, dirnames, filenames) in walk(path):
    filenames_plant = filenames
    nilai = []
    print(dirpath)
    for index, names in tqdm(enumerate(filenames_plant)):
        listarea = []
        image_src = cv2.imread(dirpath+"/"+names)
        #image_src = cv2.resize(image_src, (400, 300))
        #image_src = brigtning(image_src)
        image_hsv = cv2.cvtColor(image_src, cv2.COLOR_BGR2HSV)
        h = 30
        v = 255
        lower = np.array([h - 10, 40, v - 40])
        upper = np.array([h + 10, 255, v + 40])
        image_mask = cv2.inRange(image_hsv, lower, upper)

        #CLOSING
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(image_mask, cv2.MORPH_CLOSE, kernel)

        #BINARIZE
        ret, thresh1 = cv2.threshold(closing, 127, 255, cv2.THRESH_BINARY)

        #FIND CONTOURS
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(thresh1, contours, -1, (50, 150, 150), 4)



        print(len(contours))
        if (len(contours) > 0):
            for index, val in enumerate(contours):
                listarea.append(cv2.contourArea(contours[index]))
            print(names, "-> ", max(listarea))
            listcontourleaf.append(max(listarea))
        else:
            print(names, "-> Tidak ditemukan contour")



        #cv2.imshow("sadas",image_mask)
        #cv2.waitKey(0)
    #if(len(nilai)!=0):
        #print(dirpath+":    "+str(max(nilai))+" - "+str(min(nilai)))

print("MAX : ", max(listcontourleaf))

