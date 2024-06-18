# AlignmentOfUAVImages
## Description
This tool is designed to calculate UAV pixel coordinates in the world coordinate system using the corresponded georeferenced
satellite image. The transformation between pair of pictures calculated using key points pairs extracted from both of
images.
![visualization](https://github.com/AnNyiiik/HWThirdTerm/assets/114094098/b6596732-c49f-47cc-baa8-01f9c97bfd31)
## Usage
### 1st tool
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
### 2nd tool
1. Organise your test data in a following way: [example of data](example_of_data).
1. run command in the terminal:
`python make_data_for_unsupervised_deep_homography.py path_to_folder_with_all_the_data path_to_save`
1. pull docker image: `docker pull anyaaaaaa/unsupervised_deep_homography:version_4`
1. create a container from image: `docker run -it image_id /bin/bash`
1. copy your data into container: `docker cp path_to_data_on_your_machine container_id:/workspace/unsupervisedDeepHomographyRAL2018/data`
1. run: `docker exec -it container_id /bin/bash`
1. run: `cd code`
1. run `python homography_CNN_real.py --mode=test --batch_size=2`
1. run: `docker cp container_id:/workspace/log/results/homographies.txt path_to_copy`
1. run: `docker stop container_id`
1. run on the terminal to start the experiment:
`python experiment_2.py path_to_experimental_data_folder path_to_image_names path_to_homographies`
1. check the results in path_to_experimental_data_folder
## Experimental results
### 1st experiment
There were two sets of satellite images as sets of reference images. The first set is Google Satellite, the second is
ESRI World imagery. Both of sets were received via QGIS. The images can be seen [here](https://disk.yandex.ru/d/gnq7IZf6hADQyA).
Comparison of the maps providers' results are presented on the following hist:
![comparison](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/3bb6cb3c-b10f-48f9-ab4a-cc44f153cef9)

|     provider     | mean value for error (pixels) | max error value | min error value | standard deviation |
| ---------------- | ----------------------------- | --------------- | --------------- | ------------------ |
|      esri        |        27                     |      110        |      5          |       27           |
| google satellite |        23                     |      92         |      3          |       20           |

Reprojection errors with standard deviation value for each image in each map providers' collection:
![reprojection_error_for_each_pair_google](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/719278ed-df4c-42d2-9a8b-658313850c46)
![reprojection_error_for_each_pair](https://github.com/AnNyiiik/AlignmentOfUAVImages/assets/114094098/d271cd9f-816d-4e29-9ff7-9cef333e6033)

### 2nd experiment
There were two sets of satellite images as sets of reference images as well, but they were cut so that the final size was 640*480.
Comparison of the maps providers' results are presented on the following hist:
![reprojection_error_comparison.pdf](https://github.com/user-attachments/files/15866290/reprojection_error_comparison.pdf)

|     provider     | mean value for error (pixels) | max error value | min error value | standard deviation |
| ---------------- | ----------------------------- | --------------- | --------------- | ------------------ |
|      esri        |        243                     |      456        |      64          |       101           |
| google satellite |        285                     |      439         |      89          |       96           |

Reprojection errors with standard deviation value for each image in each map providers' collection:
![reprojection_error_google_experiment_3.pdf](https://github.com/user-attachments/files/15866309/reprojection_error_google_experiment_3.pdf)
![reprojection_error_esri_experiment_3.pdf](https://github.com/user-attachments/files/15866301/reprojection_error_esri_experiment_3.pdf)

### Comparison
Comparison of results according to images resolution
|     provider     | mean value 1st experiment | mean value 1st experiment |
| ---------------- | ----------------------------- | --------------- | 
|      esri        |        27                     |      304        |  
| google satellite |        23                     |      356        |   
