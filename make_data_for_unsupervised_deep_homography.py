import argparse
import os
from pathlib import Path
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
            Path(current_location) / 'matched_kpts_query'
        )
        key_points_satellite = alignment.read_key_points_from_file(
            Path(current_location) / 'matched_kpts_reference'
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

        aer_img = Image.open(Path(current_location) / 'uav_after_resize.png')
        width, height = aer_img.size
        corners_under_homography = (
            alignment.calculate_pixels_coordinates_in_destination_image(
                [[0, 0], [width, 0], [width, height], [0, height]], H
            )
        )

        pair_name = str(current_location).split("/")[-1]

        sat_name, aer_name = "sat_" + pair_name + ".png", "aer_" + pair_name + ".png"
        sat_img = Image.open(Path(current_location) / 'satellite_after_resize.png')
        sat_img.save(Path(path_to_batch) / sat_name)
        aer_img.save(Path(path_to_batch) / aer_name)

        with open(Path(path_to_batch) / 'test_real.txt', "a") as f:
            f.write(
                "aer_" + pair_name + ".png" + "  " + "sat_" + pair_name + ".png" + "\n"
            )

        corners_str = ' '.join(["0 0", str(width), "0", str(width), str(height), "0", str(height)])

        with open(Path(path_to_batch) / 'test_gt.txt', "a") as f:
            gt_str = corners_str + " "
            for i in range(4):
                for j in range(2):
                    gt_str += str(int(corners_under_homography[i][0][j])) + " "
            f.write(f'{gt_str}\n')

        with open(Path(path_to_batch) / 'test_pts1.txt', "a") as f:
            f.write(f'{corners_str}\n')


with open(Path(path_to_batch) / 'test_pts1.txt', "r") as f:
    lines = f.readlines()

if len(lines) % 2 != 0:
    with open(Path(path_to_batch) / 'test_pts1.txt', "a") as f:
        f.write(f'{corners_str}\n')
    with open(Path(path_to_batch) / 'test_gt.txt', "r") as f:
        last_line = f.readlines()[-1]
    with open(Path(path_to_batch) / 'test_gt.txt', "a") as f:
        f.write(last_line)
    with open(Path(path_to_batch) / 'test_real.txt', "r") as f:
        last_line = f.readlines()[-1]
    with open(Path(path_to_batch) / 'test_real.txt', "a") as f:
        f.write(last_line)
