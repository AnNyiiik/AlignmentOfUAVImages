import cv2 as cv
import numpy as np
import os

from pathlib import Path

import util
import homography_finder

class homography_finder_CNN_based(homography_finder.homography_finder):

    def align(self, img_query_path, img_reference_path):
        img_query_cropped = util.clip_image(img_query_path)
        img_reference_cropped = util.clip_image(img_reference_path)
        os.system('docker start image_name')
