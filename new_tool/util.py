import cv2 as cv
from PIL import Image

def read_key_points_from_file(path):
    with open(path, 'r') as f:
        lines = [line.rstrip() for line in f]
        key_points = list()
        for line in lines:
            point = list(map(int, line.split()))
            key_points.append(cv.KeyPoint(point[0], point[1], 1))
    return key_points

def clip_image(path_to_image, size=(240, 320)):
    image = Image.open(path_to_image)
    width, height = image.size
    original_aspect_ratio = width / height
    target_aspect_ratio = size[1]/size[0]
    if abs(original_aspect_ratio - target_aspect_ratio) < 0.001:
        return image
    if original_aspect_ratio > target_aspect_ratio:
        new_width = int(target_aspect_ratio * height)
        left = (width - new_width) // 2
        right = left + new_width
        cropped_img = image.crop((left, 0, right, height))
    else:
        new_height = int(width / target_aspect_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        cropped_img = image.crop((0, top, width, bottom))

    return cropped_img
