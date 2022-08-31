import numpy as np
import cv2 as cv


class Finder:
    def __init__(self):
        pass

    @staticmethod
    def find_item(needle, haystack, threshold=0.5):

        bmat_width = needle.shape[0]
        bmat_height = needle.shape[1]

        result = cv.matchTemplate(needle, haystack, cv.TM_CCOEFF_NORMED)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []

        for location in locations:
            rect = [int(location[0]), int(location[1]), bmat_width, bmat_height]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        center_points = []

        if len(rectangles):
            line_color = (0, 0, 255)
            line_type = cv.LINE_4

            for (x,y,w,h) in rectangles:

                # print(x, y, w, h)
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                center_points.append((center_x, center_y))

                top_left = (x, y)
                bottom_right = (x+h, y+w)

                cv.rectangle(haystack, top_left, bottom_right, color=line_color, thickness=1, lineType=line_type)
        return center_points





"""

        my_screenshot = self.capper.take_screenshot()
        my_screenshot = np.array(my_screenshot)
        my_screenshot = cv.cvtColor(my_screenshot, cv.COLOR_RGB2GRAY)

        (thresh, thing) = cv.threshold(my_screenshot, 127, 255, cv.THRESH_BINARY)
        (thresh1, thing1) = cv.threshold(self.text_not, 127, 255, cv.THRESH_BINARY)
        (thresh2, thing2) = cv.threshold(self.text_perc, 127, 255, cv.THRESH_BINARY)

        is_digging = self.find_item(needle=thing1, haystack=thing, threshold=.80)
        is_not_digging = self.find_item(needle=thing2, haystack=thing, threshold=.80)


"""
