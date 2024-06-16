import argparse
import os
from PIL import Image

import alignment

parser = argparse.ArgumentParser()
parser.add_argument(
    "path_folder_with_data",
    type=str,
    help="folder with pairs and their correspondences",
)
parser.add_argument("path_to_save_batches", type=str, help="directory with batches")
args = parser.parse_args()

path_to_batch = args.path_to_save_batches

for root, dirs, files in os.walk(args.path_folder_with_data, topdown=True):
    current_location = root
    if len(dirs) == 0:
        key_points_aerial = alignment.read_key_points_from_file(
            current_location + "/matched_kpts_query"
        )
        key_points_satellite = alignment.read_key_points_from_file(
            current_location + "/matched_kpts_reference"
        )

        if (
            len(key_points_aerial) < 4
            or len(key_points_satellite) < 4
            or len(key_points_aerial) != len(key_points_satellite)
        ):
            print("Sorry, there are too few correspondences to count transformation")
            continue

        H, mask = alignment.find_homography_transform(
            key_points_aerial, key_points_satellite
        )
        corners_under_homography = (
            alignment.calculate_pixels_coordinates_in_destination_image(
                [[0, 0], [640, 0], [640, 480], [0, 480]], H
            )
        )

        pair_name = str(current_location).split("/")[-1]

        sat_img = Image.open(current_location + "/satellite_after_resize.png")
        sat_img.save(path_to_batch + "/" + "sat_" + pair_name + ".png")
        aer_img = Image.open(current_location + "/uav_after_resize.png")
        aer_img.save(path_to_batch + "/" + "aer_" + pair_name + ".png")

        with open(path_to_batch + "/test_real.txt", "a") as f:
            f.write(
                "aer_" + pair_name + ".png" + "  " + "sat_" + pair_name + ".png" + "\n"
            )

        with open(path_to_batch + "/test_gt.txt", "a") as f:
            f.write(
                "0 0 640 0 640 480 0 480 "
                + str(int(corners_under_homography[0][0][0]))
                + " "
                + str(int(corners_under_homography[0][0][1]))
                + " "
                + str(int(corners_under_homography[1][0][0]))
                + " "
                + str(int(corners_under_homography[1][0][1]))
                + " "
                + str(int(corners_under_homography[2][0][0]))
                + " "
                + str(int(corners_under_homography[2][0][1]))
                + " "
                + str(int(corners_under_homography[3][0][0]))
                + " "
                + str(int(corners_under_homography[3][0][1]))
                + "\n"
            )

        with open(path_to_batch + "/test_pts1.txt", "a") as f:
            f.write("0 0 640 0 640 480 0 480\n")


with open(path_to_batch + "/test_pts1.txt", "r") as f:
    lines = f.readlines()

if len(lines) % 2 != 0:
    with open(path_to_batch + "/test_pts1.txt", "a") as f:
        f.write("0 0 640 0 640 480 0 480\n")
    with open(path_to_batch + "/test_gt.txt", "r") as f:
        last_line = f.readlines()[-1]
    with open(path_to_batch + "/test_gt.txt", "a") as f:
        f.write(last_line)
    with open(path_to_batch + "/test_real.txt", "r") as f:
        last_line = f.readlines()[-1]
    with open(path_to_batch + "/test_real.txt", "a") as f:
        f.write(last_line)
