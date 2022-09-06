import torch
import multiprocessing as mp
from window_capture import Screencap
from character import Character


cap = Screencap()
mike = Character()

def detect_bp():

    screen_shot = cap.take_screenshot()
    result = model(screen_shot)
    locations = result.pandas().xyxy[0]
    locations_list = list(locations.iterrows())
    mike.bp_locations = locations_list
    return locations_list

if __name__ == '__main__':
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best_seg_.938.pt')
    model.conf = .85
    climb_process = mp.Process(target=mike.always_climb)  # Commented out for testing. Un-comment these two lines when testing movement.
    climb_process.start()
    mike.position_mouse()

    while True: 
        bp_locations = detect_bp()
        mike.lazy()
