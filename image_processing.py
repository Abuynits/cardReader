import math
from random import randint

import numpy as np
import cv2

from Rectangle import Rectangle

threshold_value = 170
min_area = 50000
max_area = 10000000
image_name = "cards.JPG"


# threshold= convert to black/white depending on what value you get
# counters - detect lines

# find counters - get three arrays - first image, second is countour, and last is hirearchy
def find_rectangle_contours(img, threshold_value, min_area, max_area, rectangle_list):
    grey_scale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    otsu_ret, thresholds = cv2.threshold(grey_scale_image, threshold_value, 255, cv2.CHAIN_APPROX_NONE)
    image_contours, image_hierarchy = cv2.findContours(thresholds, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    number_cards = 0

    # cv2.imshow('cards', thresholds)
    for contour in image_contours:

        potential_contour = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        if len(potential_contour) == 4:
            (x_loc, y_loc), (width, height), angle = cv2.minAreaRect(potential_contour)
            if width * height > min_area:
                if width * height < max_area:
                    number_cards += 1
                    cv2.drawContours(img, [potential_contour], 0, (randint(0, 255), randint(0, 255), randint(0, 255)),
                                     20)

                    cv2.circle(img, (int(x_loc), int(y_loc)), 7, (255, 0, 0), 20)
                    cv2.putText(img, "card", (int(x_loc), int(y_loc) + 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 20)
                    # print("(", x_loc, ",", y_loc, ")", " angle: ", angle)
                    rect = Rectangle(x_loc, y_loc, width, height, angle)
                    pts = rect.get_rectangle_pts()

                    cv2.circle(img, pts[0], 7, (255, 0, 0), 20)

                    number_pts = rect.get_number_points()
                    for pt in number_pts:
                        cv2.circle(img, pt, 7, (0, 255, 0), 20)
                    rectangle_list.append(rect)
    print("number of cards:", number_cards)
    cv2.imshow('cards', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_greyscale_number_array(img, rectangle_array):
    get_extra_coverage = .25

    img = cv2.imread(image_name)
    grey_scale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for rectangle in rectangle_array:
        top_left_bound, top_right_bound, bottom_left_bound, bottom_right_bound = rectangle.get_number_points()

        start_x = top_left_bound[0] - top_left_bound[0] * get_extra_coverage
        start_y = top_left_bound[1] - top_left_bound[1] * get_extra_coverage
        end_x = bottom_right_bound[0] + bottom_right_bound[0] * get_extra_coverage
        end_y = bottom_right_bound[1] + bottom_right_bound[1] * get_extra_coverage

        for x_loc in range(start_x, end_x):
            for y_loc in range(start_y, end_y):
                #TODO: need to find a way to see if a point is in a polygon
                pass
                # now check if in the bounds:
                #if x_loc > top_left_bound[0] && x_loc < bottom_right_bound



rectangle_list = []
img = cv2.imread(image_name)
find_rectangle_contours(img, threshold_value, min_area, max_area, rectangle_list)

find_greyscale_number_array(image_name, rectangle_list)
