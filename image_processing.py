import math
from random import randint

import numpy as np
import cv2

threshold_value = 170
min_area = 50000
max_area = 10000000
image_name = "cards.JPG"


class Rectangle:
    def __init__(self, x, y, w, h, angle):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.angle = angle
        self.check_width()

    def get_rectangle_pts(self):
        top_left = self.get_rotation((-self.w / 2, -self.h / 2))
        top_left[0] += int(self.x)
        top_left[1] += int(self.y)
        top_right = self.get_rotation((self.w / 2, -self.h / 2))
        top_right[0] += int(self.x)
        top_right[1] += int(self.y)
        bottom_left = self.get_rotation((-self.w / 2, self.h / 2))
        bottom_left[0] += int(self.x)
        bottom_left[1] += int(self.y)
        bottom_right = self.get_rotation((self.w / 2, self.h / 2))
        bottom_right[0] += int(self.x)
        bottom_right[1] += int(self.y)
        # print("W&H: ",self.w,self.h)
        print("center", "(", self.x, ",", self.y, ")")
        print("(", top_left[0], ",", top_left[1], ")")
        print("(", top_right[0], ",", top_right[1], ")")
        print("(", bottom_left[0], ",", bottom_left[1], ")")
        print("(", bottom_right[0], ",", bottom_right[1], ")")
        print()
        return top_left, top_right, bottom_right, bottom_left

    def check_width(self):
        if self.w > self.h:
            temp = self.h
            self.h = self.w
            self.w = temp

    def get_rotation(self, point):
        # if angle is close to 90, this means that need to rotate left CCW
        # if angle is close to 0, this means to rotate right CW
        # return [point[0],point[1]]
        print("angle",self.angle)
        rotation_angle = -self.angle / 180 * math.pi
        if self.angle > 45:
            rotation_angle = (90 - self.angle) / 180 * math.pi
        print(rotation_angle)
        new_x = point[0] * math.cos(rotation_angle) + point[1] * math.sin(rotation_angle)
        new_y = -point[0] * math.sin(rotation_angle) + point[1] * math.cos(rotation_angle)
        return [int(new_x), int(new_y)]


# threshold= convert to black/white depending on what value you get
# counters - detect lines

# find counters - get three arrays - first image, second is countour, and last is hirearchy
def find_rectangle_contours(image_name, threshold_value, min_area, max_area, rectangle_list):
    img = cv2.imread(image_name)
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
                    cv2.circle(img, (pts[0][0], pts[0][1]), 7, (255, 0, 0), 20)
                    rectangle_list.append(rect)
    print("number of cards:", number_cards)
    cv2.imshow('cards', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


rectangle_list = []
find_rectangle_contours(image_name, threshold_value, min_area, max_area, rectangle_list)
# def find_greyscale_number_array(image_name, rectangle_array):
#     img = cv2.imread(image_name)
#     grey_scale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     for rectangle in rectangle_array:
#         top_left = rectangle.get_rectangle_pts()[0]
#         print(top_left)
#         cv2.circle(img, (int(top_left[0]), int(top_left[1])), 7, (0, 255, 0), 20)
#     # TODO: with my current rectangles, use affline transformation https://en.wikipedia.org/wiki/Affine_transformation
#
#
#
#
# find_greyscale_number_array(image_name, rectangle_list)
