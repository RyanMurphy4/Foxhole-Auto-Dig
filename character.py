import keyboard
import time
from math import sqrt
import mouse
import numpy as np
import cv2 as cv
from finder import Finder
from window_capture import Screencap

perc_img = cv.imread('digging_img/perc.png', cv.IMREAD_GRAYSCALE)



class Character:
    def __init__(self):
        self.px = 950
        self.py = 750
        self.bp_locations = ''
        self.center_coords = ""
        self.closest_bp = ''
        self.camera_positioned = False

        self.center_condition = False

        self.is_moving_up = False
        self.is_digging = False

    def display_attr(self):
        print(f"self.center_condition: {self.center_condition}")
        print(f"self.is_digging: {self.is_digging}")
        print(f"self.closest_bp: {self.closest_bp}")

    #Seperate process that constantly presses space, this is to avoid your character getting stuck on other blueprints/objects
    def always_climb(self):
        while True:
            keyboard.press_and_release('space')
            time.sleep(.5)

    def position_mouse(self):
        mouse.move(940, 0)

    def is_close_x(self, closest_bp):
        if closest_bp:
            px = self.px
            bx = closest_bp[0]
            return abs(px - bx) < 50

    def is_close_y(self, closest_bp):
        if closest_bp:
            py = self.py
            by = closest_bp[1]
            return abs(py - by) < 50

    def has_reached_center(self):
        self.center_condition = self.is_close_x(self.closest_bp) and self.is_close_y(self.closest_bp)

    def move_up(self):
        keyboard.press('w')


    def stop_up(self):
        keyboard.release('w')

    def start_digging(self):
        mouse.press('left')

    def stop_digging(self):
        mouse.release('left')

    def turn_camera_left(self):
        keyboard.press('.')
        time.sleep(.005)
        keyboard.release('.')

    def turn_camera_right(self):
        keyboard.press(',')
        time.sleep(.005)
        keyboard.release(',')

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

    def nav_camera(self, threshold):
        self.update_closest_bp()

        if self.closest_bp: #Avoid errors, if no BP is detected, do nothing..
            bp_x, bp_y = self.closest_bp
            if abs(bp_x - 940) > threshold: #If bp center isn't within 'threshold' amount of pixels,
                if bp_x < 940:
                    self.turn_camera_left()
                elif bp_x > 940:
                    self.turn_camera_right()

    def move_to_center(self):
        if not self.center_condition:
            self.nav_camera(40)
            self.move_up()
        elif self.center_condition:
            self.stop_up()


    def check_if_digging(self):
        screenshot = Screencap.take_screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)

        (thresh, thing) = cv.threshold(screenshot, 127, 255, cv.THRESH_BINARY)
        (thresh1, digging_bw) = cv.threshold(perc_img, 127, 255, cv.THRESH_BINARY)


        currently_digging = Finder.find_items(image=thing, img_to_match=digging_bw, debug=False, threshold=.8)


        if currently_digging:
            if len(currently_digging):
                self.is_digging = True
        else:
            self.is_digging = False

    def update_closest_bp(self):
        self.get_post_coords(self.bp_locations)
        self.closest_bp = self.get_closest(self.center_coords)

    def lazy(self):
        self.update_closest_bp()
        self.has_reached_center()

        if self.center_condition is not None:
            if not self.center_condition:
                self.move_to_center()
            else:
                if self.center_condition:
                    self.stop_up()
                if not self.is_digging:
                    time.sleep(1)
                    self.start_digging()
                    self.is_digging = True

            if not self.center_condition and self.is_digging:
                self.stop_digging()
                self.is_digging = False
        else:
            pass
        self.display_attr()