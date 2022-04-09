import math


class Rectangle:

    def __init__(self, x, y, w, h, angle):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.angle = angle
        self.check_width()
        self.greyscale_number_pixel_array = []
        self.card_number=-1

    def print_rect_debug(self, top_left, top_right, bottom_right, bottom_left):
        print("W&H: ", self.w, self.h)
        print("center", "(", self.x, ",", self.y, ")")
        print("(", top_left[0], ",", top_left[1], ")")
        print("(", top_right[0], ",", top_right[1], ")")
        print("(", bottom_left[0], ",", bottom_left[1], ")")
        print("(", bottom_right[0], ",", bottom_right[1], ")")
        print()

    def scale_from_255(self):
        for row in range(len(self.greyscale_number_pixel_array)):
            for col in range(len(self.greyscale_number_pixel_array[0])):
                val = self.greyscale_number_pixel_array[row][col]
                self.greyscale_number_pixel_array[row][col] = val / 255.0

    def get_rotated_rectangle_pts(self):
        top_left = self.get_origin_rotation((-self.w / 2, -self.h / 2))
        top_left[0] += int(self.x)
        top_left[1] += int(self.y)
        top_right = self.get_origin_rotation((self.w / 2, -self.h / 2))
        top_right[0] += int(self.x)
        top_right[1] += int(self.y)
        bottom_left = self.get_origin_rotation((-self.w / 2, self.h / 2))
        bottom_left[0] += int(self.x)
        bottom_left[1] += int(self.y)
        bottom_right = self.get_origin_rotation((self.w / 2, self.h / 2))
        bottom_right[0] += int(self.x)
        bottom_right[1] += int(self.y)

        self.print_rect_debug(top_left, top_right, bottom_right, bottom_left)

        return top_left, top_right, bottom_right, bottom_left

    def get_unrotated_rectangle_pts(self):
        top_left = int(self.x - self.w / 2), int(self.y - self.h / 2)
        top_right = int(self.x + self.w / 2), int(self.y - self.h / 2)
        bottom_left = int(self.x - self.w / 2), int(self.y + self.h / 2)
        bottom_right = int(self.x + self.w / 2), int(self.y + self.h / 2)
        return top_left, top_right, bottom_right, bottom_left

    def get_number_scaled_width_height(self):
        return int(self.w * 0.35), int(self.h * 0.35)

    def get_rotated_number_points(self):
        # TODO: potentially add min scale factors as well to remove noise

        max_width_scale_factor = 0.35
        max_height_scale_factor = 0.35
        top_left_card = self.get_origin_rotation((-self.w / 2, -self.h / 2))
        top_left_card[0] += int(self.x)
        top_left_card[1] += int(self.y)
        top_right_card = self.get_origin_rotation((-(self.w / 2) * (1 - max_width_scale_factor), -self.h / 2))
        top_right_card[0] += int(self.x)
        top_right_card[1] += int(self.y)
        bottom_left_card = self.get_origin_rotation((-(self.w / 2), -(self.h / 2) * (1 - max_height_scale_factor)))
        bottom_left_card[0] += int(self.x)
        bottom_left_card[1] += int(self.y)
        bottom_right_card = self.get_origin_rotation(
            (-(self.w / 2) * (1 - max_width_scale_factor), -(self.h / 2) * (1 - max_height_scale_factor)))
        bottom_right_card[0] += int(self.x)
        bottom_right_card[1] += int(self.y)
        return top_left_card, top_right_card, bottom_left_card, bottom_right_card

    def get_unrotated_number_points(self):
        min_width = 0.97
        min_height = 0.97

        max_width = 0.65
        max_height = 0.65

        top_left_card = int(self.x - self.w / 2 * min_width), int(self.y - self.h / 2 * min_height)
        top_right_card = int(self.x - (self.w / 2) * max_width), int(self.y - self.h / 2 * min_height)
        bottom_left_card = int(self.x - (self.w / 2 * min_width)), int(self.y - (self.h / 2) * max_height)
        bottom_right_card = int(self.x - (self.w / 2) * max_width), int(
            self.y - (self.h / 2) * max_height)

        return top_left_card, top_right_card, bottom_left_card, bottom_right_card

    def check_width(self):
        if self.w > self.h:
            temp = self.h
            self.h = self.w
            self.w = temp

    def get_origin_rotation(self, point):
        # if angle is close to 90, this means that need to rotate left CCW
        # if angle is close to 0, this means to rotate right CW
        # return [point[0],point[1]]

        rotation_angle = -self.angle / 180 * math.pi
        if self.angle > 45:
            rotation_angle = (90 - self.angle) / 180 * math.pi

        new_x = point[0] * math.cos(rotation_angle) + point[1] * math.sin(rotation_angle)
        new_y = -point[0] * math.sin(rotation_angle) + point[1] * math.cos(rotation_angle)
        return [int(new_x), int(new_y)]

    def get_rotation_about_point(self, point):
        # if angle is close to 90, this means that need to rotate left CCW
        # if angle is close to 0, this means to rotate right CW
        # return [point[0],point[1]]
        x_loc = point[0] - self.x
        y_loc = point[1] - self.y

        rotation_angle = -self.angle / 180 * math.pi
        if self.angle > 45:
            rotation_angle = (90 - self.angle) / 180 * math.pi

        new_x = x_loc * math.cos(rotation_angle) + y_loc * math.sin(rotation_angle)
        new_y = -x_loc * math.sin(rotation_angle) + y_loc * math.cos(rotation_angle)

        new_x = new_x + self.x
        new_y = new_y + self.y

        return [int(new_x), int(new_y)]

    def get_width_height(self):
        return self.w, self.h
