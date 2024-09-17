import cv2 as cv
import numpy as np
import os
import shutil

from pathlib import Path
from accessify import private

import scripts.util as util
import scripts.homography_finder as homography_finder


class homography_finder_feature_based(homography_finder.homography_finder):
    @private
    def find_correspondences(self, img_query_path, img_reference_path):
        img_query = cv.imread(img_query_path)
        img_reference = cv.imread(img_reference_path)

        absolute_path = Path("~/AlignmentOfUAVImages").expanduser()

        (
            query_saved_path,
            reference_saved_path,
        ) = util.create_temporary_folders_for_images(
            img_query, img_reference, os.path.join(absolute_path, "feature_method_data")
        )
        query_folder = Path(query_saved_path).parent
        reference_folder = Path(reference_saved_path).parent

        if not os.path.exists(
            os.path.join(absolute_path, "feature_based_method_results")
        ):
            os.mkdir(os.path.join(absolute_path, "feature_based_method_results"))
        path_to_save = os.path.join(absolute_path, "feature_based_method_results")

        sg_weights_path = Path(
            "~/aero-vloc/aerial_vloc_weights/superglue_outdoor.pth"
        ).expanduser()
        script_path = Path("~/aero-vloc/simple_two_images_matching.py").expanduser()
        os.system(
            f"python {script_path} {query_folder} {reference_folder} {path_to_save} {sg_weights_path} >/dev/null 2>&1"
        )
        query_pts = util.read_key_points_from_file(
            os.path.join(path_to_save, "matched_kpts_query")
        )
        reference_pts = util.read_key_points_from_file(
            os.path.join(path_to_save, "matched_kpts_reference")
        )

        shutil.rmtree(os.path.join(absolute_path, "feature_method_data"))
        shutil.rmtree(path_to_save)

        return query_pts, reference_pts

    @private
    def find_homography_transform(self, query_pts, reference_pts):
        source = [[key_point.pt[0], key_point.pt[1]] for key_point in query_pts]
        dest = [[key_point.pt[0], key_point.pt[1]] for key_point in reference_pts]
        H, _ = cv.findHomography(np.array(source), np.array(dest), cv.RANSAC)
        return H

    """the method finds a homography matrix between two images: 1st - UAV's, 2nd - satellite's
    the method uses feature-based method to find a transformation
    and takes images paths, if there is no transformation between images it returns null
    """

    def align(self, img_query_path, img_reference_path):
        if not os.path.exists(os.path.abspath(img_query_path)):
            raise FileNotFoundError(f"file {img_query_path} does not exist")
        elif not os.path.exists(os.path.abspath(img_reference_path)):
            raise FileNotFoundError(f"file {img_reference_path} does not exist")
        else:
            query_pts, reference_pts = self.find_correspondences(
                img_query_path, img_reference_path
            )
            if len(query_pts) == 0:
                return None
            return self.find_homography_transform(query_pts, reference_pts)
