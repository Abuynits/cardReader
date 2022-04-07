from random import randint

import numpy as np
import cv2

threshold_value = 140
min_area = 2000
image_name = "cards.JPG"


class Rectangle:
    def __init__(self, x, y, w, h, center_x, center_y):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center_x = center_x
        self.center_y = center_y


# threshold= convert to black/white depending on what value you get
# counters - detect lines

# find counters - get three arrays - first image, second is countour, and last is hirearchy
def find_rectangle_contours(image_name, threshold_value, min_area):
    img = cv2.imread(image_name)
    grey_scale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    otsu_ret, thresholds = cv2.threshold(grey_scale_image, threshold_value, 255, cv2.CHAIN_APPROX_NONE)
    image_contours, image_hierarchy = cv2.findContours(thresholds, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    number_cards = 0
    rectangle_list = []
    for contour in image_contours:

        potential_contour = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        if len(potential_contour) == 4:
            x_loc, y_loc, width, height = cv2.boundingRect(potential_contour)
            if width * height > min_area:
                if x_loc != 0 and y_loc != 0:
                    number_cards += 1
                    cv2.drawContours(img, [potential_contour], 0, (randint(0, 255), randint(0, 255), randint(0, 255)),
                                     20)
                    centerX = int(x_loc + width / 2)
                    centerY = int(y_loc + height / 2)
                    cv2.circle(img, (centerX, centerY), 7, (255, 0, 0), 20)
                    cv2.putText(img, "card", (centerX, centerY + 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 20)
                    rectangle_list.append(Rectangle(x_loc, y_loc, width, height, centerX, centerY))
    print("number of cards:", number_cards)

    cv2.imshow('cards', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return rectangle_list


find_rectangle_contours(image_name, threshold_value, min_area)
