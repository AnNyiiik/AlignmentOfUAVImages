import alignment
import argparse
import cv2 as cv
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import statistics

parser = argparse.ArgumentParser()
parser.add_argument("path_folder_with_data", type=str)

# parse arguments
args = parser.parse_args()
errors = list()
#set experiment for each pair in subdirectory
for (root,dirs,files) in os.walk(args.path_folder_with_data, topdown=True):
        current_location = root
        if len(dirs) == 0:
        # read all key points for UAV and satellite images
            key_points_aerial = alignment.read_key_points_from_file(current_location + '/matched_kpts_query')
            key_points_satellite = alignment.read_key_points_from_file(current_location + '/matched_kpts_reference')

            if (
                len(key_points_aerial) < 4
                or len(key_points_satellite) < 4
                or len(key_points_aerial) != len(key_points_satellite)
            ):
                print("Sorry, there are too few correspondences to count transformation")
                continue
            aerial_image = cv.imread(current_location + "/uav_after_resize.png")
            satellite_image = cv.imread(current_location + "/satellite_after_resize.png")

            # find and draw matches
            pair_indexes = [j for j in range(len(key_points_aerial))]
            matches = [cv.DMatch(i, i, 1) for i in range(len(key_points_aerial))]
            image_matches = alignment.draw_matches(
                matches, aerial_image, satellite_image, key_points_aerial, key_points_satellite
            )
            cv.imwrite("image_matches.png", image_matches)

            # compute homography transform
            H = alignment.find_homography_transform(key_points_aerial, key_points_satellite)
            # count reprojection error
            points_before_homography = [[key_points_aerial[j].pt[0], key_points_aerial[j].pt[1]] for j in range(len(key_points_aerial))]
            points_under_homography = alignment.calculate_pixels_coordinates_in_destination_image(points_before_homography, H)
            truth_points = [[key_points_satellite[j].pt[0], key_points_satellite[j].pt[1]] for j in range(len(key_points_satellite))]

            error, declines = alignment.find_reprojection_error(
                truth_points, points_under_homography
            )
            errors.append(error)

            # save hist of reprojection error and its value to the experiment results folder
            with open(current_location + "/reprojection_error", "w") as f:
                f.write("reprojection error: " + str(error) + "\n")

            sns.displot(declines, kde=True, bins=len(key_points_aerial), color = 'darkblue')
            plt.savefig(
                current_location + "/reprojection_error.png",
                bbox_inches="tight",
                pad_inches=1,
                transparent=True,
                facecolor="w",
                edgecolor="b",
                orientation="landscape",
            )
#count mean and standard deviation
if (len(errors) > 0):
    standard_deviation = statistics.stdev(errors)
    mean = statistics.mean(errors)
    min = min(errors)
    max = max(errors)

    #save results of experiment
    with open(args.path_folder_with_data + "/experimentResults.txt", 'w') as f:
        f.write("standard deviation: " + str(standard_deviation) + "\n")
        f.write("expectancy value: " + str(mean) + "\n")
        f.write("min value: " + str(min) + "\n")
        f.write("min value: " + str(min))

    #create graphic
    err = [standard_deviation for i in range(len(errors))]
    df = pd.DataFrame(errors)
    df.plot(kind="bar", title='Reprojection error for each pair (UAV + satellite)', ylabel='meters', yerr=err)
    plt.savefig(args.path_folder_with_data + "/reprojection_error_for_each_pair.png")