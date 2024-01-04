import matplotlib.pyplot as plt
import sys
from alignment import *
import statistics

#parse arguments
if len(sys.argv) != 6:
    print("incorrect number of args, should be 5")
else:
    pathToAerialKeyPoints, pathToSatelliteKeyPoints, pathToAerialImage, pathToSatelliteImage, pathToMetaData = sys.argv[1], \
                                                                                                     sys.argv[2], \
                                                                                                     sys.argv[3], \
                                                                                                     sys.argv[4], \
                                                                                                     sys.argv[5]
    # read all key points for UAV and satellite images
    keyPointsAerial = readKeyPointsFromFile(pathToAerialKeyPoints)
    keyPointsSatellite = readKeyPointsFromFile(pathToSatelliteKeyPoints)

    if len(keyPointsAerial) < 4 or len(keyPointsSatellite) < 4:
        print("Sorry, there sre too few correspondences to count transformation")

    aerialImage = cv.imread(pathToAerialImage)
    satelliteImage = cv.imread(pathToSatelliteImage)

    # read pixel coordinates of UAV image to count its (lat, lon) coordinates, read satellite image corners' coordinates
    with open(pathToMetaData, 'r') as f:
        lat_left, lon_left = map(float, f.readline().split())
        lat_right, lon_right = map(float, f.readline().split())
        X, Y = map(int, f.readline().split())

    # find and draw matches
    pairIndexes = [j for j in range(len(keyPointsAerial))]
    matches = findMatches(pairIndexes)
    imageMatches = drawMatches(matches, aerialImage, satelliteImage, keyPointsAerial, keyPointsSatellite)
    cv.imwrite("image_matches.png", imageMatches)

    # compute homography transform
    H = findHomographyTransform(keyPointsAerial, keyPointsSatellite, matches)

    # count reprojection error
    points_under_homography = [[0] * 2 for j in range(len(keyPointsAerial))]
    truth_points = [[0] * 2 for j in range(len(keyPointsAerial))]
    for j in range(len(keyPointsAerial)):
        destPoint = np.array(H).dot(np.array([keyPointsAerial[matches[j].queryIdx].pt[0],
                                              keyPointsAerial[matches[j].queryIdx].pt[1], 1]))
        points_under_homography[j][0], points_under_homography[j][1] = destPoint[0], destPoint[1]
        truth_points[j][0], truth_points[j][1] = keyPointsSatellite[j].pt[0], keyPointsSatellite[j].pt[1]

    error, declines = findReprojectionError(truth_points, points_under_homography)

    # count pixel coordinates
    lat, lon = countPixelCoordinates(aerialImage, (X, Y), satelliteImage, H, (lat_left, lon_left),
                                     (lat_right, lon_right))

    # save hist of reprojection error and its value to the experiment results folder
    f = open("results", 'w')
    f.write("reprojection error: " + str(error))
    f.write("standard deviation of reprojection error: " + str(statistics.stdev(declines)))
    f.write("pixel coordinates (lat, lon): " + str(lat) + " " + str(lon))
    f.close()
    plt.hist(declines, color='blue', edgecolor='black', bins=len(keyPointsAerial))
    plt.savefig("reprojection_error.png",
                bbox_inches="tight",
                pad_inches=1,
                transparent=True,
                facecolor="w",
                edgecolor='b',
                orientation='landscape')
