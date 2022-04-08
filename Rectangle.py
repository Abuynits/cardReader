import math


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

       # self.print_rect_debug(top_left, top_right, bottom_right, bottom_left)

        return top_left, top_right, bottom_right, bottom_left

    def get_number_points(self):
        #TODO: potentially add min scale factors as well to remove noise
        width_scale_factor = 0.35
        height_scale_factor = 0.35
        top_left_card = self.get_rotation((-self.w / 2, -self.h / 2))
        top_left_card[0] += int(self.x)
        top_left_card[1] += int(self.y)
        top_right_card = self.get_rotation((-(self.w / 2) * (1 - width_scale_factor), -self.h / 2))
        top_right_card[0] += int(self.x)
        top_right_card[1] += int(self.y)
        bottom_left_card = self.get_rotation((-(self.w / 2), -(self.h / 2)*(1-height_scale_factor)))
        bottom_left_card[0] += int(self.x)
        bottom_left_card[1] += int(self.y)
        bottom_right_card = self.get_rotation((-(self.w / 2) * (1 - width_scale_factor), -(self.h / 2)*(1-height_scale_factor)))
        bottom_right_card[0] += int(self.x)
        bottom_right_card[1] += int(self.y)
        return top_left_card,top_right_card,bottom_left_card,bottom_right_card
    def print_rect_debug(self, top_left, top_right, bottom_right, bottom_left):
        print("W&H: ", self.w, self.h)
        print("center", "(", self.x, ",", self.y, ")")
        print("(", top_left[0], ",", top_left[1], ")")
        print("(", top_right[0], ",", top_right[1], ")")
        print("(", bottom_left[0], ",", bottom_left[1], ")")
        print("(", bottom_right[0], ",", bottom_right[1], ")")
        print()

    def check_width(self):
        if self.w > self.h:
            temp = self.h
            self.h = self.w
            self.w = temp

    def get_rotation(self, point):
        # if angle is close to 90, this means that need to rotate left CCW
        # if angle is close to 0, this means to rotate right CW
        # return [point[0],point[1]]

        rotation_angle = -self.angle / 180 * math.pi
        if self.angle > 45:
            rotation_angle = (90 - self.angle) / 180 * math.pi

        new_x = point[0] * math.cos(rotation_angle) + point[1] * math.sin(rotation_angle)
        new_y = -point[0] * math.sin(rotation_angle) + point[1] * math.cos(rotation_angle)
        return [int(new_x), int(new_y)]
