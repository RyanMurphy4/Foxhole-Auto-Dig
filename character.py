import keyboard
import time
from math import sqrt

import mouse


class Character:
    def __init__(self):
        self.bp_locations = ''

    def always_climb(self):
        while True:
            keyboard.press_and_release('space')
            time.sleep(.5)

    def position_mouse(self):
        mouse.move(940, 0)

    def get_post_coords(self, location_list):
        center_xy_list = []
        for location in location_list:
            x_min = location[1][0]
            y_min = location[1][1]
            x_max = location[1][2]
            y_max = location[1][3]
            center_x = ((x_max - x_min) / 2) + x_min
            center_y = ((y_max - y_min) / 2) + y_min

            center_xy_list.append((center_x, center_y))

        return center_xy_list

    def get_closest(self, list_of_coordinates):
        x1, y1 = (750, 950)
        closest_point = ""
        lowest_distance = 10_000  # High initial value to insure
        for point in list_of_coordinates:
            x2 = point[0]
            y2 = point[1]
            distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Distance formula
            if distance < lowest_distance:
                lowest_distance = distance
                closest_point = (x2, y2)

        return closest_point

