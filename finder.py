import numpy as np
import cv2 as cv


class Finder:
    def __init__(self):
        pass

    @staticmethod
    def find_items(image, img_to_match, debug=False, threshold=0.9):
        box_centers = []

        # Get width and height of image to match
        w = img_to_match.shape[0]
        h = img_to_match.shape[1]

        # Matches the template with instances in the image
        res = cv.matchTemplate(image,img_to_match, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if loc[0].size == 0 and loc[1].size == 0:
            return None # NOTE: You probably want code to check if return == None

        for pt in zip(*loc[::-1]):
            # Finds center of box 
            box_center = ((pt[0] + w + pt[0]) / 2, (pt[1] + h + pt[1]) / 2)
            box_centers.append(box_center)

            if debug:
                cv.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
        if debug:
            cv.imwrite('res.jpg', image)

        
        return box_centers 