import cv2 as cv
import numpy as np
import os

from pathlib import Path
from accessify import private

import util
import homography_finder


class homography_finder_feature_based(homography_finder.homography_finder):
    @private
    def find_correspondences(self, img_query_path, img_reference_path):
        ##copy images to temporary folder
        img_query = cv.imread(img_query_path)
        img_reference = cv.imread(img_reference_path)

        absolute_path = Path("~/AlignmentOfUAVImages").expanduser()

        (
            query_saved_path,
            reference_saved_path,
        ) = util.create_temporary_folders_for_images(img_query, img_reference)
        query_folder = query_saved_path.parent
        reference_folder = reference_saved_path.parent

        if not absolute_path.joinpath("feature_based_method_results").exists():
            os.mkdir(absolute_path.joinpath("feature_based_method_results"))
        path_to_save = absolute_path.joinpath("feature_based_method_results")

        sg_weights_path = Path(
            "~/aero-vloc/aerial_vloc_weights/superglue_outdoor.pth"
        ).expanduser()
        ##find points
        script_path = Path("~/aero-vloc/simple_two_images_matching.py").expanduser()
        os.system(
            f"python {script_path} {query_folder} {reference_folder} {path_to_save} {sg_weights_path} >/dev/null 2>&1"
        )
        ##read points
        query_pts = util.read_key_points_from_file(
            path_to_save.joinpath("matched_kpts_query")
        )
        reference_pts = util.read_key_points_from_file(
            path_to_save.joinpath("matched_kpts_reference")
        )
        return query_pts, reference_pts

    @private
    def find_homography_transform(self, query_pts, reference_pts):
        source = [[key_point.pt[0], key_point.pt[1]] for key_point in query_pts]
        dest = [[key_point.pt[0], key_point.pt[1]] for key_point in reference_pts]
        H, _ = cv.findHomography(np.array(source), np.array(dest), cv.RANSAC)
        return H

    def align(self, img_query_path, img_reference_path):
        ##find correspondences
        query_pts, reference_pts = self.find_correspondences(
            img_query_path, img_reference_path
        )
        return self.find_homography_transform(query_pts, reference_pts)
