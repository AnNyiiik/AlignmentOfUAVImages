import cv2 as cv
import numpy as np
import os

from PIL import Image
from pathlib import Path

import util
import homography_finder

class homography_finder_CNN_based(homography_finder.homography_finder):

    def align(self, img_query_path, img_reference_path):
        img_query_cropped = util.clip_image(img_query_path)
        img_reference_cropped = util.clip_image(img_reference_path)

        absolute_path = Path('~/AlignmentOfUAVImages').expanduser()
        if not absolute_path.joinpath("uav").exists():
            os.mkdir(absolute_path.joinpath("uav"))
        query_saved_path = absolute_path.joinpath("uav/query.jpg")
        img_query_cropped.save(query_saved_path)

        if not absolute_path.joinpath("sat").exists():
            os.mkdir(absolute_path.joinpath("sat"))
        reference_saved_path = absolute_path.joinpath("sat/reference.jpg")
        img_reference_cropped.save(reference_saved_path)

        os.system('docker start 39be30bf5915')

        os.system(f'docker cp {absolute_path.joinpath("uav/query.jpg")} 39be30bf5915:/workspace/unsupervisedDeepHomographyRAL2018/data/query.png')
        os.system(f'docker cp {absolute_path.joinpath("sat/reference.jpg")} 39be30bf5915:/workspace/unsupervisedDeepHomographyRAL2018/data/reference.png')

        os.system('docker exec -it 39be30bf5915 /bin/bash')



