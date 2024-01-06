import cv2 as cv
import numpy as np
import math

distance_for_match = 1.7976931348623157e308


def read_key_points_from_file(path):
    with open(path, "r") as f:
        lines = [line.rstrip() for line in f]
    key_points = list()
    for line in lines:
        point = list(map(int, line.split()))
        key_points.append(cv.KeyPoint(point[0], point[1], 1))
    return key_points


def calculate_point_in_destination_image(image_source, pixel, homography_matrix):
    height, width = image_source.shape[:2]
    if pixel.pt[0] < 0 or pixel.pt[0] > width:
        return
    if pixel.pt[1] < 0 or pixel.pt[1] > height:
        return
    point_in_destination_image = np.array(homography_matrix).dot(
        np.array([pixel.pt[0], pixel.pt[1], 1])
    )
    return point_in_destination_image


def calculate_pixel_coordinates(
    image_source,
    pixel,
    destination_image,
    homography_matrix,
    coordinates_of_top_left,
    coordinates_of_bottom_right,
):
    height, width = image_source.shape[:2]
    pixel = cv.KeyPoint(pixel[0], pixel[1], 1)
    if pixel.pt[0] < 0 or pixel.pt[0] > width:
        return
    if pixel.pt[1] < 0 or pixel.pt[1] > height:
        return
    point_in_destination_image = calculate_point_in_destination_image(
        image_source, pixel, homography_matrix
    )
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
    img_matches = np.empty(
        (
            max(aerial_image.shape[0], satellite_image.shape[0]),
            aerial_image.shape[1] + satellite_image.shape[1],
            3,
        ),
        dtype=np.uint8,
    )
    cv.drawMatches(
        aerial_image,
        key_points_aerial,
        satellite_image,
        key_points_satellite,
        matches,
        img_matches,
        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    return img_matches


def find_homography_transform(key_points_aerial, key_points_satellite):
    source = [
        [key_points_aerial[i].pt[0], key_points_aerial[i].pt[1]]
        for i in range(len(key_points_aerial))
    ]
    dest = [
        [key_points_satellite[i].pt[0], key_points_satellite[i].pt[1]]
        for i in range(len(key_points_aerial))
    ]
    H, _ = cv.findHomography(np.array(source), np.array(dest), cv.RANSAC)
    return H


def find_matches(pair_indexes):
    matches = []
    for pair in pair_indexes:
        matches.append(cv.DMatch(pair, pair, distance_for_match))
    return matches


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
