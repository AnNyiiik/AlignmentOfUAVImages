import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import statistics
import os

from pathlib import Path
from progress.bar import IncrementalBar

'''the method creates data for a cnn-based method which finds a homography between two images'''
def make_data_for_CNN_method(width_query, height_query, H):
    corners_under_homography = calculate_pixels_coordinates_in_destination_image(
        [[0, 0], [width_query, 0], [width_query, height_query], [0, height_query]], H
    )

    absolute_path = Path("~/AlignmentOfUAVImages").expanduser()

    if not os.path.exists(os.path.join(absolute_path, "CNN_based_method_data")):
        os.mkdir(os.path.join(absolute_path, "CNN_based_method_data"))
    CNN_based_method_data = os.path.join(absolute_path, "CNN_based_method_data")

    with open(os.path.join(CNN_based_method_data, "test_real.txt"), "w") as f:
        f.write(
            "query.jpg"
            + "  "
            + "reference.jpg"
            + "\n"
            + "query.jpg"
            + "  "
            + "reference.jpg"
        )
    images_names_path = os.path.join(CNN_based_method_data, "test_real.txt")

    corners_str = f"0 0 {width_query} 0 {width_query} {height_query} 0 {height_query}"

    corners_under_homography_str = ""
    for i in range(4):
        for j in range(2):
            corners_under_homography_str += " " + str(
                int(corners_under_homography[i][0][j])
            )

    with open(os.path.join(CNN_based_method_data, "test_gt.txt"), "w") as f:
        f.write(
            corners_str
            + corners_under_homography_str
            + "\n"
            + corners_str
            + corners_under_homography_str
        )
    gt_path = os.path.join(CNN_based_method_data, "test_gt.txt")

    with open(os.path.join(CNN_based_method_data, "test_pts1.txt"), "w") as f:
        f.write(corners_str + "\n" + corners_str)
    query_corners_path = os.path.join(CNN_based_method_data, "test_pts1.txt")

    return images_names_path, gt_path, query_corners_path, CNN_based_method_data

'''the method finds coordinates of a query image pixel in reference image according to a homography transformation 
between images'''
def calculate_pixels_coordinates_in_destination_image(pixels, homography_matrix):
    points_under_homography = cv.perspectiveTransform(
        np.array(pixels, dtype=np.float32).reshape(-1, 1, 2), homography_matrix
    )
    for i in range(len(pixels)):
        norm = np.linalg.norm(
            np.array(homography_matrix[2]).dot([pixels[i][0], pixels[i][1], 1])
        )
        points_under_homography[i][0][0] = int(points_under_homography[i][0][0] / norm)
        points_under_homography[i][0][1] = int(points_under_homography[i][0][1] / norm)
    return points_under_homography

'''the method finds coordinates of a UAV's image pixel according to the homography transformation between UAV's image and 
satellite image 
it takes reference image, pixel coordinates into UAV image, homography matrix, geo-coordinates of top left and bottom right 
corners of the reference image'''
def calculate_pixel_coordinates(
    image_reference,
    pixel,
    homography_matrix,
    coordinates_of_top_left,
    coordinates_of_bottom_right,
):
    height, width = image_reference.shape[:2]

    point_in_destination_image = calculate_pixels_coordinates_in_destination_image(
        [pixel], homography_matrix
    )[0][0]
    lat = coordinates_of_top_left[0] + float(
        point_in_destination_image[1]
    ) / height * float((coordinates_of_bottom_right[0] - coordinates_of_top_left[0]))
    lon = coordinates_of_top_left[1] + float(
        point_in_destination_image[0]
    ) / width * float((coordinates_of_bottom_right[1] - coordinates_of_top_left[1]))
    return lat, lon

'''the method clips images according to a predefined proportion'''
def clip_image(path_to_image, size=(240, 320)):
    image = cv.imread(path_to_image)
    height, width, _ = image.shape
    original_aspect_ratio = width / height
    target_aspect_ratio = size[1] / size[0]
    if abs(original_aspect_ratio - target_aspect_ratio) < 0.001:
        return image
    if original_aspect_ratio > target_aspect_ratio:
        new_width = int(target_aspect_ratio * height)
        left = (width - new_width) // 2
        right = left + new_width
        cropped_img = image[0 : height + 1, left : right + 1]
    else:
        new_height = int(width / target_aspect_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        cropped_img = image[top : bottom + 1, 0 : width + 1]

    return cropped_img

'''the returnes a docker container's name by its id'''
def get_container_id_by_name(client, name):
    try:
        container_id = (
            list(
                filter(
                    lambda container: container.name == name,
                    client.containers.list(all=True),
                )
            )
            .pop()
            .id
        )
        return container_id
    except:
        print(f"the container {name} doesn't exist")

'''the method reads key points from file and returns a list of a key points'''
def read_key_points_from_file(path):
    with open(path, "r") as f:
        lines = [line.rstrip() for line in f]
        key_points = list()
        for line in lines:
            point = list(map(int, line.split()))
            key_points.append(cv.KeyPoint(point[0], point[1], 1))
    return key_points

'''the method reads a homography matrix from file'''
def read_homography_matrix_from_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
    matrix = list()
    for line in lines:
        line = line.replace("]", "")
        line = line.replace("[", "")
        nums = list(map(float, line.split()))
        matrix.append(nums)
    matrix = np.array(matrix)
    return matrix

'''the method creates a temporary folder with all needed data for a method, which finds homography transformation between images'''
def create_temporary_folders_for_images(img_query, img_reference, path_to_folders):
    absolute_path = os.path.abspath(path_to_folders)
    if not os.path.exists(os.path.join(absolute_path, "uav")):
        os.makedirs(os.path.join(absolute_path, "uav"))
    query_saved_path = os.path.join(absolute_path, "uav/query.jpg")
    cv.imwrite(str(query_saved_path), img_query)

    if not os.path.exists(os.path.join(absolute_path, "sat")):
        os.mkdir(os.path.join(absolute_path, "sat"))
    reference_saved_path = os.path.join(absolute_path, "sat/reference.jpg")
    cv.imwrite(str(reference_saved_path), img_reference)
    return query_saved_path, reference_saved_path

'''the method finds reprojection error according to a homography transformation and ground truth correspondences
it takes homography matrix, path to file with key points in a query images, path to file with key points in a reference image'''
def find_reprojection_error(H_pred, path_to_uav_gt_corr, path_to_sat_gt_corr):
    uav_kpts = read_key_points_from_file(path_to_uav_gt_corr)
    uav_kpts = [[uav_kpts[i].pt[0], uav_kpts[i].pt[1]] for i in range(len(uav_kpts))]
    sat_kpts = read_key_points_from_file(path_to_sat_gt_corr)
    sat_kpts = [[sat_kpts[i].pt[0], sat_kpts[i].pt[1]] for i in range(len(sat_kpts))]
    uav_kpts_H_pred_transformed = calculate_pixels_coordinates_in_destination_image(
        uav_kpts, H_pred
    )
    error = 0
    for i in range(len(uav_kpts)):
        decline = np.linalg.norm(sat_kpts[i] - uav_kpts_H_pred_transformed[i])
        error += decline
    return error / len(uav_kpts)

'''the method finds reprojection errors for a set of images pairs, then it returns mean and standard deviation values'''
def set_experiment(path_to_data, pair_names, kpts_files, method, method_name):
    errors = list()
    bar = IncrementalBar(max=len(pair_names))
    print(f"Processing the {path_to_data} with {method_name}")
    for pair, pair_kpts in zip(pair_names, kpts_files):
        aer, sat = pair.split()
        aer = os.path.join(path_to_data, aer)
        print(aer)
        sat = os.path.join(path_to_data, sat)
        aer_kpts, sat_kpts = pair_kpts.split()
        aer_kpts = os.path.join(path_to_data, aer_kpts)
        sat_kpts = os.path.join(path_to_data, sat_kpts)
        H_pred = method.align(aer, sat)
        reprojection_error = find_reprojection_error(H_pred, aer_kpts, sat_kpts)
        errors.append(reprojection_error)
        bar.next()
    bar.finish()
    mean, dev = statistics.mean(errors), statistics.stdev(errors)
    return errors, mean, dev

'''the method saves all the results of an experiment to a given file'''
def save_experiment_results(folder_to_save, method_name, map_name, mean, dev, errors):
    with open(
        os.path.join(
            folder_to_save, f"{method_name}_method_with_{map_name}_map_results.txt"
        ),
        "w",
    ) as f:
        f.write(
            f"reprojection error mean val: {mean}\nreprojection error standart deviation val: {dev}"
        )
    with open(
        os.path.join(
            folder_to_save, f"{method_name}_method_with_{map_name}_map_errors.txt"
        ),
        "w",
    ) as f:
        for error in errors:
            f.write(f"{error}\n")


def draw_box_plot(data, path_to_save, box_labels, colors=["#faf75c"]):
    fig, ax = plt.subplots()
    ax.set_ylabel("Ошибка репроекции в пикселях")
    plt.title("Блочная диаграмма с ограничителями выбросов")

    bplot = ax.boxplot(data, patch_artist=True, tick_labels=box_labels)

    if len(colors) == 1:
        for patch in bplot["boxes"]:
            patch.set_facecolor(colors[0])
    else:
        for patch, color in zip(bplot["boxes"], colors):
            patch.set_facecolor(color)

    for median in bplot["medians"]:
        median.set(color="red", linewidth=3)

    for flier in bplot["fliers"]:
        flier.set(color="#e7298a", alpha=0.5)

    plt.savefig(path_to_save)
