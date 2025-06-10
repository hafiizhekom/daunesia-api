import cv2
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog

image_hsv = None
pixel = (0, 0, 0)  # RANDOM DEFAULT VALUE

ftypes = [
    ('JPG', '*.jpg;*.JPG;*.JPEG'),
    ('PNG', '*.png;*.PNG'),
    ('GIF', '*.gif;*.GIF'),
]

def findSignificantContours (img, edgeImg):
    image, contours, heirarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)

    # From among them, find the contours with large surface area.
    significant = []
    tooSmall = edgeImg.size * 5 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
    for tupl in level1:
        contour = contours[tupl[0]];
        area = cv2.contourArea(contour)
        if area > tooSmall:
            significant.append([contour, area])

            # Draw the contour on the original image
            cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.LINE_AA, maxLevel=1)

    significant.sort(key=lambda x: x[1])
    #print ([x[1] for x in significant]);
    return [x[0] for x in significant];


def brigtning(img):
    global image_hsv
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

    img_resize_result = cv2.resize(img, (int(width / 10), int(height / 10)), interpolation=cv2.INTER_CUBIC)
    img = img_resize_result
    if (height < width) and (height != width):
        dst = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    else:
        dst = img
    crop_img = dst[55:355, 0:300]
    return crop_img

def denoising(img):
    height, width = img.shape[:2]
    real = img
    img = cv2.medianBlur(img, 5)

    return img

def pick_color(event, x, y, flags, param):
    global image_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]

        # HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.

        # lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        #upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])

        lower = np.array([30 - 10, 40, 255-40])
        upper = np.array([30 + 10, 255, 255])

        tepatnya = np.array([pixel[0], pixel[1], pixel[2]])
        print(lower, upper, tepatnya)

        # A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS


        #fgbg = cv2.createBackgroundSubtractorMOG2()
        #edgeImg_8u = np.asarray(edgeImg, np.uint8)

        # Find contours
        #significant = findSignificantContours(image_hsv, edgeImg_8u)


        image_mask = cv2.inRange(image_hsv, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(image_mask, cv2.MORPH_CLOSE, kernel)
        ret, thresh1 = cv2.threshold(closing, 127, 255, cv2.THRESH_BINARY)

        #image_mask = fgbg.apply(image_src)
        #image_mask =  cv2.Canny(image_mask,100,200)

        contours, hierarchy  = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(thresh1, contours, -1, (50, 150, 150), 4)
        #cnt = contours[0]
        #m = cv2.moments(cnt)
        #area = cv2.contourArea(cnt)
        print(len(contours))
        #print(area)

        listarea = []
        if (len(contours) > 0):
            for index, val in enumerate(contours):
                listarea.append(cv2.contourArea(contours[index]))

        if(len(listarea)>0):
            print(max(listarea))
        else:
            print("List Area Kosong")

        cv2.imshow("Mask", image_mask)


def main():
    global image_hsv, pixel    , image_src

    # OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw()  # HIDE THE TKINTER GUI
    file_path = filedialog.askopenfilename(initialdir = "/home/hafiizhekom/PycharmProjects/LCRestAPI/data/temporary")
    image_src = cv2.imread(file_path)
    #image_src = crop_rotate(image_src)
    #image_src = brigtning(image_src)
    #image_src = denoising(image_src)
    cv2.imshow("BGR", image_src)


    # CREATE THE HSV FROM THE BGR IMAGE
    image_hsv = cv2.cvtColor(image_src, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", image_hsv)

    # CALLBACK FUNCTION
    cv2.setMouseCallback("HSV", pick_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()