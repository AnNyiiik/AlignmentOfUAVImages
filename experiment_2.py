import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics

import alignment

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("path_to_folder_with_data", type=str)
parser.add_argument("path_to_image_names_pairs", type=str)
parser.add_argument("path_to_homographies", type=str)
args = parser.parse_args()

homographies = list()

with open(args.path_to_homographies, "r") as f:
    lines = f.readlines()
    for i in range(int(len(lines) / 3)):
        H_lines = lines[i * 3 : (i + 1) * 3]
        matrix = list()
        for line in H_lines:
            line = line.replace("]", "")
            line = line.replace("[", "")
            nums = list(map(float, line.split()))
            matrix.append(nums)
        homographies.append(np.array(matrix))

pair_names = list()
with open(args.path_to_image_names_pairs, "r") as f:
    pair_names = f.readlines()

errors = list()
for i in range(1, len(pair_names) + 1):
    pair = str(i)

    aer_pts_path = args.path_to_folder_with_data + "/" + pair + "/matched_kpts_query"
    key_points_aerial = alignment.read_key_points_from_file(aer_pts_path)
    sat_pts_path = aer_pts_path.replace("query", "reference")
    key_points_sat = alignment.read_key_points_from_file(sat_pts_path)
    H = homographies[i]
    points_before_homography = [
        [key_points_aerial[j].pt[0], key_points_aerial[j].pt[1]]
        for j in range(len(key_points_aerial))
    ]
    points_under_homography = (
        alignment.calculate_pixels_coordinates_in_destination_image(
            points_before_homography, H
        )
    )
    truth_points = [
        [key_points_sat[j].pt[0], key_points_sat[j].pt[1]]
        for j in range(len(key_points_sat))
    ]

    error, declines = alignment.find_reprojection_error(
        truth_points, points_under_homography
    )
    errors.append(error)

standard_deviation = statistics.stdev(errors)
mean = statistics.mean(errors)
min = min(errors)
max = max(errors)

with open(args.path_to_folder_with_data + "/experiment_results.txt", "w") as f:
    f.write("standard deviation: " + str(standard_deviation) + "\n")
    f.write("expectancy value: " + str(mean) + "\n")
    f.write("min value: " + str(min) + "\n")
    f.write("max value: " + str(max))

# create graphic
err = [standard_deviation for i in range(len(errors))]
df = pd.DataFrame(errors, columns=None)
df.plot(
    kind="bar",
    title="Reprojection error for each pair (UAV + satellite image)",
    ylabel="pixels",
    yerr=err,
    xlabel="pairs of images",
    color="#2E8B57",
)
plt.savefig(args.path_to_folder_with_data + "/reprojection_error.png")
