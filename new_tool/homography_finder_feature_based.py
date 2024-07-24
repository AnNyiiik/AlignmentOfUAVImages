import cv2 as cv
import numpy as np
import os

from pathlib import Path

import dataloader
import homography_finder

class homography_finder_feature_based(homography_finder):

    def find_correspondences(self, img_query_path, img_reference_path):
        ##copy images to temporary folder
        img_query = cv.imread(img_query_path)
        img_reference = cv.imread(img_reference_path)

        root = os.path.expanduser('~')

        os.mkdir(root + "/uav")
        cv.imwrite(root + "/uav/query.jpg", img_query)
        query_saved_path = root + "/uav/query.jpg"

        os.mkdir(root + "/sat")
        cv.imwrite(root + "/sat/reference.jpg", img_reference)
        reference_saved_path = root + "/sat/query.jpg"

        os.mkdir(root + "/feature_based_method_results")
        path_to_save = root + "/feature_based_method_results"
        sg_weights = "jaiosisjiao"
        ##find points
        os.system(f"python aero-vloc/simple_two_images.matching.py {query_saved_path} {reference_saved_path} {path_to_save} {sg_weights}")
        ##read points
        query_pts = dataloader.read_key_points_from_file()
        reference_pts = dataloader.read_key_points_from_file()
        return query_pts, reference_pts

    def find_homography_transform(self, query_pts, reference_pts):
        source = [[key_point.pt[0], key_point.pt[1]] for key_point in query_pts]
        dest = [[key_point.pt[0], key_point.pt[1]] for key_point in reference_pts]
        H, mask = cv.findHomography(np.array(source), np.array(dest), cv.RANSAC)
        return H, mask

    def align(self, img_query_path, img_reference_path):
        ##find correspondences
        query_pts, reference_pts = self.find_correspondences(img_query_path, img_reference_path)
        return self.find_homography_transform(query_pts, reference_pts)
