# AlignmentOfUAVImages
## Description
This tool is designed to calculate UAV pixel coordinates in the world coordinate system using the corresponded georeferenced
satellite image. The transformation between pair of pictures can be calculated by two methods: 1st - the feature based method
(it finds the common features in the pair of images and then chooses the most appropriate transformation which satisfies 
all the correspondences not excluded by RANSAC algorithm), 2nd - the method which applies the CNN model to find the matrix 
of the transformation. 
![visualization](https://github.com/AnNyiiik/HWThirdTerm/assets/114094098/b6596732-c49f-47cc-baa8-01f9c97bfd31)
## Usage
1. Clone the repository running `git clone git@github.com:AnNyiiik/AlignmentOfUAVImages.git` on a terminal.
1. Install all the requirements: `pip install -r requirements.txt`.
1. For the feature based method the following tool should be installed: [https://github.com/prime-slam/aero-vloc.git](https://github.com/prime-slam/aero-vloc.git).
1. To ran an experiment with several map-providers organise your data in a following way (ground truth data should be provided to perform the experiment): 
   [https://drive.google.com/drive/folders/1Nqc-FdZtgT9UT2JHNSXQLRhyjKrG37c3?usp=sharing](https://drive.google.com/drive/folders/1Nqc-FdZtgT9UT2JHNSXQLRhyjKrG37c3?usp=sharing)
1. Ran a command on a terminal: `python path_to_experiment_script --paths_to_data="your paths" --maps="maps_names" --file_with_pair_names="file_with_names_of_aer_and_sat_pics_to_align"
   --file_with_kpts_names="file_with_file_names_which_contains_gt_correspondences" --path_folder_to_save_results="path" --draw_plot="False or True" --colors="list_of_the_colors_codes"` 
## Experimental results
The aim of the experiment was to reveal the best configuration (map + method) according to the query aerial data, which 
was provided by Skoltech laboratory. There were two sets of satellite images as sets of reference images. The first set 
is Google Satellite, the second -- ESRI World imagery. 
Comparison of the configurations' results are presented on the following box plot and table:


![plot](https://github.com/user-attachments/assets/412ff88b-c7a3-402c-8297-45aea598c5dd)

|     provider     | mean value for error (pixels) | standard deviation | min error value | max error value |
| ---------------- | ----------------------------- | --------------- | --------------- | ------------------ |
|      feature + google        |          26                   |      19        |       4         |          100        |
| feature + esri |            39                 |        90       |         4       |       564           |
| CNN + google |            284                 |       104        |          97      |           447       |
| CNN + esri |           244                  |        96       |       32         |        440          |