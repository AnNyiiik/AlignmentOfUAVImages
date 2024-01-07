import cv2 as cv
import numpy as np

def read_key_points_from_file(path):
    with open(path, "r") as f:
        lines = [line.rstrip() for line in f]
    key_points = list()
    for line in lines:
        point = list(map(int, line.split()))
        key_points.append(cv.KeyPoint(point[0], point[1], 1))
    return key_points

def calculate_pixel_coordinates(
    image_source,
    pixel,
    homography_matrix,
    coordinates_of_top_left,
    coordinates_of_bottom_right,
):
    height, width = image_source.shape[:2]
    if pixel[0] < 0 or pixel[0] > width:
        return
    if pixel[1] < 0 or pixel[1] > height:
        return
    pixel = np.array(pixel).reshape(-1,1,2).astype(np.float32)
    point_in_destination_image = cv.perspectiveTransform(pixel, homography_matrix)

    lat = coordinates_of_top_left[0] + float(
        point_in_destination_image[1]
    ) / height * float((coordinates_of_bottom_right[0] - coordinates_of_top_left[0]))
    lon = coordinates_of_top_left[1] + float(
        point_in_destination_image[0]
    ) / width * float((coordinates_of_bottom_right[1] - coordinates_of_top_left[1]))
    return lat, lon

def draw_matches(
    matches, aerial_image, satellite_image, key_points_aerial, key_points_satellite
):
    img_matches = cv.drawMatches(
        aerial_image,
        key_points_aerial,
        satellite_image,
        key_points_satellite,
        matches,
        None,
    )
    return img_matches

def find_homography_transform(key_points_aerial, key_points_satellite):
    source = [[key_point.pt[0], key_point.pt[1]] for key_point in key_points_aerial]
    dest = [[key_point.pt[0], key_point.pt[1]] for key_point in key_points_satellite]
    H, _ = cv.findHomography(np.array(source), np.array(dest), cv.RANSAC)
    return H

def find_reprojection_error(points_truth, points_under_homography):
    if len(points_truth) == 0:
        return
    error = 0
    declines = []
    points_truth = np.array(points_truth)
    points_under_homography = np.array(points_under_homography)
    for i in range(len(points_truth)):
        decline = np.linalg.norm(points_truth[i] - points_under_homography[i])
        declines.append(decline)
        error += decline
    return error / len(points_truth), declines