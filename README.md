# AlignmentOfUAVImages
### Description
This tool is designed to calculate UAV pixel coordinates in the world coordinate system using the corresponded georeferenced 
satellite image. The transformation between pair of pictures calculated using key points pairs extracted from both of 
images. 
![visualization](https://github.com/AnNyiiik/HWThirdTerm/assets/114094098/b6596732-c49f-47cc-baa8-01f9c97bfd31)
### Usage
1. Clone the repository running `git clone git@github.com:AnNyiiik/AlignmentOfUAVImages.git` on a terminal.
1. Add your data to the repository root folder. See how it must be organised here (structure of data folder and its 
   subdirectories should be the same, as well as names of files): [example of data](example_of_data).
1. Run the command to execute the experiment: `python3 experiment.py PATH_TO_DATA_FOLDER`.
1. The image with matched key points, hist of reprojection error, file with the reprojection error value are located in 
   each subdirectory:
   * image_matches.png
   * reprojection_error.png
   * reprojection_error 
 
    The expectancy value of reprojection error for the whole collection and the diagram are located in the data folder:
   * experimentResults.txt
   * reprojection_error_for_each_pair.png
### Experimental results
There were two sets of satellite images as sets of reference images. The first set is Google Satellite, the second is
ESRI World imagery. Both of sets were received via QGIS. The images can be seen [here](https://disk.yandex.ru/d/gnq7IZf6hADQyA). 
Comparison of the maps providers' results are presented on the following hist:
![Figure_1](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/5028db40-87d8-49ad-84a2-bab50ff2a338)

|     provider     | mean value for error (pixels) | max error value | min error value | standard deviation |
| ---------------- | ----------------------------- | --------------- | --------------- | ------------------ |
|      esri        |        28.54                  |      110.43     |      6.97       |       25.62        |
| google satellite |        24.76                  |      142.89     |      4.05      |       24.43         |

Reprojection errors with standard deviation value for each image in each map providers' collection:
![reprojection_error_for_each_pair](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/326ee9f6-9459-4aa1-adba-83e31e385c05)

![reprojection_error_for_each_pair](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/d0f54d73-d3bd-42f9-8d8b-026bca82b5bf)