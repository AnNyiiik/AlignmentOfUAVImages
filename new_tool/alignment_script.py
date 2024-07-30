import homography_finder_feature_based

homography_finder = homography_finder_feature_based.homography_finder_feature_based()
H = homography_finder.align("/Users/annnikolaeff/Desktop/uav_after_resize.png", "/Users/annnikolaeff/Desktop/satellite_after_resize.png")
print(H[0])