# AlignmentOfUAVImages
### Description
This tool is designed to calculate UAV pixel coordinates in the world coordinate system using the corresponded georeferenced 
satellite image. The transformation between pair of pictures calculated using key points pairs extracted from both of 
images. 
![visualization](https://github.com/AnNyiiik/HWThirdTerm/assets/114094098/b6596732-c49f-47cc-baa8-01f9c97bfd31)
### Usage
1. Clone the repository running `git clone git@github.com:AnNyiiik/AlignmentOfUAVImages.git` on a terminal.
1. Add your data to the repository root folder  [example of data](exampleOfData).
1. Run the command to execute the experiment: `python3 experiment.py PATH_TO_UAV_KEYPOINTS PATH_TO_SATELLITE_KEYPOINTS 
   PATH_TO_UAV_IMAGE PATH_TO_SATELLITE_IMAGE PATH_TO_META_DATA`.
1. The image with matched key points, hist of reprojection error, file with the reprojection error value, 
   standard deviation of error and pixel coordinates are:
   * image_matches.png
   * reprojection_error.png
   * results 
### Experimental results
There were two sets of satellite images as sets of reference images. The first set is Google Satellite, the second is
ESRI World imagery. Both of sets were received via QGIS. The images can be seen [here](). Comparison of the maps providers'
results are presented on the following hist:
![reprojection_error](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/87e2674e-cbad-4e74-aa00-03b90db246b5)

|     provider     | mean value for error | max error value | min error value | 
| ---------------- | -------------------- | --------------- | --------------- |
|      esri        |        1.145         |      6.334      |      0.182      |
| google satellite |        0.892         |      4.577      |      0.165      |
Reprojection errors with standard deviation value for each image in each map providers' collection:
![reprojection_error_esri](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/e45db05a-83a3-4a1e-bee4-e22da7579473)
![google_sat_error](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/98e2dc14-e7e0-4333-9944-f4d3097fd6c4)