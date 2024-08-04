import homography_finder_feature_based
import homography_finder_CNN_based

homography_finder = homography_finder_CNN_based.homography_finder_CNN_based()
homography_finder.align("/Users/annnikolaeff/Desktop/uav_after_resize.png", "/Users/annnikolaeff/Desktop/satellite_after_resize.png")