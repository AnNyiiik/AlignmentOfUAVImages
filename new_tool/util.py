import cv2 as cv
import docker
import numpy as np
import os

from pathlib import Path

def make_data_for_CNN_method(width_query, height_query, H):

    corners_under_homography = calculate_pixels_coordinates_in_destination_image(
        [[0, 0], [width_query, 0], [width_query, height_query], [0, height_query]], H
    )

    absolute_path = Path('~/AlignmentOfUAVImages').expanduser()

    if not absolute_path.joinpath("CNN_based_method_data").exists():
        os.mkdir(absolute_path.joinpath("CNN_based_method_data"))
    CNN_based_method_data = absolute_path.joinpath("CNN_based_method_data")

    with open(CNN_based_method_data.joinpath("test_real.txt"), 'w') as f:
        f.write("query.jpg" + "  " + "reference.jpg" + "\n" + "query.jpg" + "  " + "reference.jpg")
    images_names_path = CNN_based_method_data.joinpath("test_real.txt")

    corners_str = f'0 0 {width_query} 0 {width_query} {height_query} 0 {height_query}'
    corners_under_homography_str = ""
    for i in range(4):
        for j in range(2):
            corners_under_homography_str += " " + str(int(corners_under_homography[i][0][j]))

    with open(CNN_based_method_data.joinpath("test_gt.txt"), 'w') as f:
        f.write(corners_str + corners_under_homography_str + "\n" + corners_str + corners_under_homography_str)
    gt_path = CNN_based_method_data.joinpath("test_gt.txt")

    with open(CNN_based_method_data.joinpath("test_pts1.txt"), 'w') as f:
        f.write(corners_str + "\n" + corners_str)
    query_corners_path = CNN_based_method_data.joinpath("test_pts1.txt")

    return images_names_path, gt_path, query_corners_path


def calculate_pixels_coordinates_in_destination_image(pixels, homography_matrix):
    points_under_homography = cv.perspectiveTransform(
        np.array(pixels).reshape(-1, 1, 2).astype(np.float32), homography_matrix
    )
    for i in range(len(pixels)):
        norm = np.linalg.norm(
            np.array(homography_matrix[2]).dot([pixels[i][0], pixels[i][1], 1])
        )
        points_under_homography[i][0][0] = int(points_under_homography[i][0][0] / norm)
        points_under_homography[i][0][1] = int(points_under_homography[i][0][1] / norm)
    return points_under_homography

def clip_image(path_to_image, size=(240, 320)):
    image = cv.imread(path_to_image)
    height, width, _ = image.shape
    original_aspect_ratio = width / height
    target_aspect_ratio = size[1]/size[0]
    if abs(original_aspect_ratio - target_aspect_ratio) < 0.001:
        return image
    if original_aspect_ratio > target_aspect_ratio:
        new_width = int(target_aspect_ratio * height)
        left = (width - new_width) // 2
        right = left + new_width
        cropped_img = image[0:height + 1, left:right + 1]
    else:
        new_height = int(width / target_aspect_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        cropped_img = image[top:bottom + 1, 0:width + 1]

    return cropped_img

def get_container_id_by_name(client, name):
    try:
        container_id = list(
            filter(lambda container: container.name == name, client.containers.list(all=True))).pop().id
        return container_id
    except:
        print(f"the container {name} doesn't exist")

def read_key_points_from_file(path):
    with open(path, 'r') as f:
        lines = [line.rstrip() for line in f]
        key_points = list()
        for line in lines:
            point = list(map(int, line.split()))
            key_points.append(cv.KeyPoint(point[0], point[1], 1))
    return key_points

def read_homography_matrix_from_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
    matrix = list()
    for line in lines:
        line = line.replace(']', '')
        line = line.replace('[', '')
        nums = list(map(float, line.split()))
        matrix.append(nums)
    matrix = np.array(matrix)
    return matrix

def create_temporary_folders_for_images(img_query, img_reference):
    absolute_path = Path('~/AlignmentOfUAVImages').expanduser()
    if not absolute_path.joinpath("uav").exists():
        os.mkdir(absolute_path.joinpath("uav"))
    query_saved_path = absolute_path.joinpath("uav/query.jpg")
    cv.imwrite(query_saved_path, img_query)

    if not absolute_path.joinpath("sat").exists():
        os.mkdir(absolute_path.joinpath("sat"))
    reference_saved_path = absolute_path.joinpath("sat/reference.jpg")
    cv.imwrite(reference_saved_path, img_reference)
    return query_saved_path, reference_saved_path