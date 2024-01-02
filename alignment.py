import cv2 as cv
import numpy as np
import math

def readKeyPointsFromFile(path):
    with open(path, 'r') as f:
        lines = [line.rstrip() for line in f]
    f.close()
    keyPoints = list()
    for line in lines:
        point = list(map(int, line.split()))
        keyPoints.append(cv.KeyPoint(point[0], point[1], 1))
    return keyPoints

def countPixelCoordinates(imageSource, pixel, destinationImage, homographyMatrix, coordinatesOfTopLeft,
                          coordinatesOfBottomRight):
    height, width = imageSource.shape[:2]
    pixel = cv.KeyPoint(pixel[0], pixel[1], 1)
    if (pixel.pt[0] < 0 or pixel.pt[0] > width):
        return
    if (pixel.pt[1] < 0 or pixel.pt[1] > height):
        return
    height, width = destinationImage.shape[:2]
    pointInDestinationImage = np.array(homographyMatrix).dot(np.array([pixel.pt[0], pixel.pt[1], 1]))
    print(pointInDestinationImage[0], pointInDestinationImage[1])
    lat = coordinatesOfTopLeft[0] + float(pointInDestinationImage[1]) / height * float((coordinatesOfBottomRight[0] -
                                                                                        coordinatesOfTopLeft[0]))
    lon = coordinatesOfTopLeft[1] + float(pointInDestinationImage[0]) / width * float((coordinatesOfBottomRight[1] -
                                                                                       coordinatesOfTopLeft[1]))
    return lat, lon

def drawMatches(matches, aerial_Image, satellite_Image, keyPointsAerial, keyPointsSatellite):
    img_matches = np.empty(
        (max(aerial_Image.shape[0], satellite_Image.shape[0]), aerial_Image.shape[1] + satellite_Image.shape[1], 3),
        dtype=np.uint8)
    cv.drawMatches(aerial_Image, keyPointsAerial, satellite_Image, keyPointsSatellite, matches,
                   img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return img_matches

def findHomographyTransform(keyPointsAerial, keyPointsSatellite, matches):
    source = np.empty((len(matches), 2), dtype=np.float32)
    reference = np.empty((len(matches), 2), dtype=np.float32)
    for i in range(len(matches)):
        source[i, 0] = keyPointsAerial[matches[i].queryIdx].pt[0]
        source[i, 1] = keyPointsAerial[matches[i].queryIdx].pt[1]
        reference[i, 0] = keyPointsSatellite[matches[i].trainIdx].pt[0]
        reference[i, 1] = keyPointsSatellite[matches[i].trainIdx].pt[1]
    H, _ = cv.findHomography(source, reference, cv.RANSAC)
    return H

def findMatches(pairIndexes):
    matches = []
    for pair in pairIndexes:
        matches.append(cv.DMatch(pair, pair, 1.7976931348623157e+308))
    return matches

def findReprojectionError(points_truth, points_under_homography):
    if (len(points_truth) == 0):
        return
    error = 0
    declines = []
    for i in range(len(points_truth)):
        decline = math.sqrt(math.pow(points_truth[i][0] - points_under_homography[i][0], 2) + \
                 math.pow(points_truth[i][1] - points_under_homography[i][1], 2))
        declines.append(decline)
        error += decline
    return error / len(points_truth), declines