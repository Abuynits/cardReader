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
                    pts = rect.get_rotated_rectangle_pts()

                    cv2.circle(img, pts[0], 7, (255, 0, 0), 20)

                    number_pts = rect.get_rotated_number_points()
                    for pt in number_pts:
                        cv2.circle(img, pt, 7, (0, 255, 0), 20)
                    rectangle_list.append(rect)
    print("number of cards:", number_cards)


def find_greyscale_number_array(img, rectangle_array):
    grey_scale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for rectangle in rectangle_array:
        top_left_number_bound, top_right_number_bound, bottom_left_number_bound, bottom_right_number_bound = rectangle.get_unrotated_number_points()

        width = int(rectangle.get_width_height()[0])
        height = int(rectangle.get_width_height()[1])

        pixel_array = [[0 for i in range(width)] for j in range(height)]

        array_x_loc = 0
        # print(len(grey_scale_image))
        # print(len(grey_scale_image[0]))
        for y_loc in range(int(top_left_number_bound[0]), int(top_right_number_bound[0])):
            array_y_loc = 0
            for x_loc in range(int(top_left_number_bound[1]), int(bottom_left_number_bound[1])):
                rotated_pt = rectangle.get_rotation((x_loc, y_loc))

                # print("image array loc:", array_x_loc, array_y_loc)
                # print("unrotated pixel array loc:", x_loc, y_loc)
                # print("rotated pixel array loc:", rotated_pt[0], rotated_pt[1])
                # print("value", grey_scale_image[rotated_pt[0]][rotated_pt[1]], end='\n\n')
                pixel_array[array_x_loc][array_y_loc] = grey_scale_image[rotated_pt[0]][rotated_pt[1]]

                array_y_loc += 1
            array_x_loc += 1

        #TODO: have an array of pixels around the number
        #TODO: need to resize the array while take the average and converting it to a 28x28 pixel array
        #TODO: then convert the array to a 1D array and give it to the rectangle object
        pixel_array = np.resize(pixel_array, (10,10))  # resize the pixel array to 28x28
        np_2d_array = np.array(pixel_array)
        rectangle.greyscale_number_pixel_array = np_2d_array.flatten().tolist()
        print(rectangle.greyscale_number_pixel_array)
        #

        # for x in range(0, height):
        #     for y in range(0, width):
        #         print(pixel_array[x][y], end=",")
        #     print()


rectangle_list = []
img = cv2.imread(image_name)
find_rectangle_contours(img, threshold_value, min_area, max_area, rectangle_list)

find_greyscale_number_array(img, rectangle_list)
cv2.imshow('cards', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
