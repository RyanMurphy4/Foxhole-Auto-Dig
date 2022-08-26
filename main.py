import torch
import numpy as np
import pandas
import multiprocessing as mp
from finder import Finder
from window_capture import Screencap
from test_data import Character

cap = Screencap()
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best_seg_.938.pt')
mike = Character()


def detect_posts():

    post_xy_locations = []
    screen_shot = cap.take_screenshot()
    result = model(screen_shot)
    locations = result.pandas().xyxy[0]
    locations_list = list(locations.iterrows())
    return locations_list


def get_post_coords(location_list):
    center_xy_list = []
    for location in location_list:
        x_min = location[1][0]
        y_min = location[1][1]
        x_max = location[1][2]
        y_max = location[1][3]
        center_x = ((x_max - x_min) / 2) + x_min
        center_y = ((y_max - y_min) / 2) + y_min
        post_confidence = location[1][4]


        center_xy_list.append((center_x, center_y))

    return center_xy_list

def center_coords(return_dictionary):
    temp_location_list = detect_posts()
    temp_center_list = get_post_coords(temp_location_list)

    return_dictionary['temp_center_list'] = temp_center_list

if __name__ == '__main__':
    manager = mp.Manager()
    return_dictionary = manager.dict()
    the_process = mp.Process(target=center_coords, args=(return_dictionary,))
    the_process.run()

    print(return_dictionary.values())
