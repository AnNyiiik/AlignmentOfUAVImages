import alignment
import argparse
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import statistics
import sys

parser = argparse.ArgumentParser()
parser.add_argument("path_to_UAV_key_points", type=str, nargs=1)
parser.add_argument("path_to_satellite_key_points", type=str, nargs=1)
parser.add_argument("path_to_UAV_image", type=str, nargs=1)
parser.add_argument("path_to_satellite_image", type=str, nargs=1)
parser.add_argument("path_to_meta_data", type=str, nargs=1)

# parse arguments
args = parser.parse_args()
print(args.path_to_UAV_key_points)
# read all key points for UAV and satellite images
key_points_aerial = alignment.read_key_points_from_file(args.path_to_UAV_key_points[0])
key_points_satellite = alignment.read_key_points_from_file(
    args.path_to_satellite_key_points[0]
)

if (
    len(key_points_aerial) < 4
    or len(key_points_satellite) < 4
    or len(key_points_aerial) != len(key_points_satellite)
):
    print("Sorry, there sre too few correspondences to count transformation")

aerial_image = cv.imread(args.path_to_UAV_image[0])
satellite_image = cv.imread(args.path_to_satellite_image[0])

# read pixel coordinates of UAV image to count its (lat, lon) coordinates, read satellite image corners' coordinates
with open(args.path_to_meta_data[0], "r") as f:
    lat_left, lon_left = map(float, f.readline().split())
    lat_right, lon_right = map(float, f.readline().split())
    X, Y = map(int, f.readline().split())

# find and draw matches
pair_indexes = [j for j in range(len(key_points_aerial))]
matches = alignment.find_matches(pair_indexes)
image_matches = alignment.draw_matches(
    matches, aerial_image, satellite_image, key_points_aerial, key_points_satellite
)
cv.imwrite("image_matches.png", image_matches)

# compute homography transform
H = alignment.find_homography_transform(key_points_aerial, key_points_satellite)

# count reprojection error
points_under_homography = [[0] * 2 for j in range(len(key_points_aerial))]
truth_points = [[0] * 2 for j in range(len(key_points_aerial))]
for j in range(len(key_points_aerial)):
    dest_point = alignment.calculate_point_in_destination_image(
        aerial_image, key_points_aerial[j], H
    )
    points_under_homography[j][0], points_under_homography[j][1] = (
        dest_point[0],
        dest_point[1],
    )
    truth_points[j][0], truth_points[j][1] = (
        key_points_satellite[j].pt[0],
        key_points_satellite[j].pt[1],
    )

error, declines = alignment.find_reprojection_error(
    truth_points, points_under_homography
)

# count pixel coordinates
lat, lon = alignment.calculate_pixel_coordinates(
    aerial_image,
    (X, Y),
    satellite_image,
    H,
    (lat_left, lon_left),
    (lat_right, lon_right),
)

# save hist of reprojection error and its value to the experiment results folder
with open("results", "w") as f:
    f.write("reprojection error: " + str(error) + "\n")
    f.write(
        "standard deviation of reprojection error: "
        + str(statistics.stdev(declines))
        + "\n"
    )
    f.write("pixel coordinates (lat, lon): " + str(lat) + " " + str(lon) + "\n")

plt.hist(declines, color="blue", edgecolor="black", bins=len(key_points_aerial))
plt.savefig(
    "reprojection_error.png",
    bbox_inches="tight",
    pad_inches=1,
    transparent=True,
    facecolor="w",
    edgecolor="b",
    orientation="landscape",
)
