import keyboard
import time
from math import sqrt
import mouse
from window_capture import Screencap


class Character:
    def __init__(self):
        self.px = 750
        self.py = 950
        self.bp_locations = ''
        self.center_coords = ""
        self.closest_bp = ''
        self.camera_positioned = False

        self.reached_center = False

        self.is_moving_up = False
        self.reached_bp = False

    #Seperate process that constantly presses space, this is to avoid your character getting stuck on other blueprints/objects
    def always_climb(self):
        while True:
            keyboard.press_and_release('space')
            time.sleep(.5)

    def position_mouse(self):
        mouse.move(940, 0)

    #Takes a list of locations that contains the top left and bottom right of bounding boxes surrounding the blueprints
    #then finds the center of the bounding box.

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
            self.center_coords = center_xy_list

        return center_xy_list

    #Uses the distance formula to find the blueprint that is located closest to the position (750, 950) which is where
    #your character is located when your mouse is positioned in the top center of your screen.
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

        self.closest_bp = closest_point
        return closest_point

    def is_close_x(self, closest_bp):
        px = self.px
        bx = closest_bp[0]
        return abs(px - bx) < 25

    def is_close_y(self, closest_bp):
        py = self.py
        by = closest_bp[1]
        return abs(py - by) < 25
    
    def move_up(self):
        # if py > by:
        keyboard.press('w')
        self.is_moving_up = True

    def stop_up(self):
        # if self.is_close_y():
        keyboard.release('w')
        self.is_moving_up = False


    def turn_camera_left(self):
        keyboard.press('.')
        time.sleep(.001)
        keyboard.release('.')

    def turn_camera_right(self):
        keyboard.press(',')
        time.sleep(.001)
        keyboard.release(',')

    def reached_center(self):
        if self.is_close_x(self.closest_bp) and self.is_close_y(self.closest_bp):
            return True





    '''
    Attempting to line top middle of screen up with center of blueprint.
    '''

    def nav_camera(self, locations):
        self.get_post_coords(locations)
        self.closest_bp = self.get_closest(self.center_coords)

        if self.closest_bp: #Avoid errors, if no BP is detected, do nothing..
            bp_x, bp_y = self.closest_bp

            if not self.camera_positioned:
                if abs(bp_x - 940) > 40:
                    if bp_x < 940:
                        self.turn_camera_left()
                    elif bp_x > 940:
                        self.turn_camera_right()
                else:
                    # self.camera_positioned = True
                    print("Lined up them lines.")

