# AlignmentOfUAVImages
### Description
This tool is designed to calculate UAV pixel coordinates in the world coordinate system using the corresponded satellite
image. The transformation between pair of pictures calculated using key points pairs extracted from both of images. 
![key points for pair of images to calculate transformation](https://github.com/AnNyiiik/HWThirdTerm/pull/1#discussion_r1441538792)
### Usage
1. Clone the repository running `git clone git@github.com:AnNyiiik/AlignmentOfUAVImages.git` on a terminal.
1. Add your data to the repository root folder  [example of data](exampleOfData).
1. Build docker image running `docker build -t alignment .`
1. Create a container using image id: `docker start container id`.
1. Run the command to execute the experiment: `python3 experiment.py path\to\UAV\KeyPoints path\to\satellite\KeyPoints 
   path\to\UAV\image path\to\satellite\image path\to\meta\data`.
1. The image with matched key points, hist of reprojection error, file with the reprojection error value, 
   standard deviation of error and pixel coordinates are:
   * image_matches.png
   * reprojection_error.png
   * results 
### Experimental results
There were two sets of satellite images as sets of reference images. The first set is Google Satellite, the second is
ESRI World imagery. Both of sets were received via QGIS. Image collections can be received [here](). The reprojection 
error value and its standard deviation for each pair is presented in the following table:

| pair  | provider         | reprojection error | standard deviation |
| ----- | ---------------- | ------------------ | ------------------ |
|   1   | Google Satellite |        6.992       |       4.989        |
|   1   | ESRI             |                    |                    |
|   2   | Google Satellite |        67.732      |       21.852       |
|   2   | ESRI             |                    |                    |
|   3   | Google Satellite |        5.725       |       5.726        |
|   3   | ESRI             |                    |                    |
|   4   | Google Satellite |        17.406      |       8.976        |
|   4   | ESRI             |                    |                    |
|   5   | Google Satellite |        48.742      |       25.956       |
|   5   | ESRI             |                    |                    |
|   6   | Google Satellite |        13.793      |       7.956        |
|   6   | ESRI             |                    |                    |
|   7   | Google Satellite |        10.439      |       7.216        |
|   7   | ESRI             |                    |                    |
|   8   | Google Satellite |        10.649      |       6.998        |
|   8   | ESRI             |                    |                    |
|   9   | Google Satellite |        9.949       |       7.214        |
|   9   | ESRI             |                    |                    |
|   10  | Google Satellite |        58.22       |       33.047       |
|   10  | ESRI             |                    |                    |
|   11  | Google Satellite |        9.734       |       7.432        |
|   11  | ESRI             |                    |                    |
|   12  | Google Satellite |        54.113      |       24.658       |
|   12  | ESRI             |                    |                    |
|   13  | Google Satellite |        28.272      |       12.118       |
|   13  | ESRI             |                    |                    |
|   14  | Google Satellite |        13.428      |       8.248        |
|   14  | ESRI             |                    |                    |
|   15  | Google Satellite |        19.919      |       9.261        |
|   15  | ESRI             |                    |                    |
|   16  | Google Satellite |        21.415      |       10.885       |
|   16  | ESRI             |                    |                    |
|   17  | Google Satellite |        73.242      |       35.844       |
|   17  | ESRI             |                    |                    |
|   18  | Google Satellite |        4.720       |       2.488        |
|   18  | ESRI             |                    |                    |
|   19  | Google Satellite |        6.709       |       4.163        |
|   19  | ESRI             |                    |                    |
|   20  | Google Satellite |        28.223      |       12.586       |
|   20  | ESRI             |                    |                    |
|   21  | Google Satellite |        5.454       |       3.974        |
|   21  | ESRI             |                    |                    |
|   22  | Google Satellite |        7.096       |       4.607        |
|   22  | ESRI             |                    |                    |
|   23  | Google Satellite |        4.122       |       2.377        |
|   23  | ESRI             |                    |                    |
|   24  | Google Satellite |        14.080      |       9.090        |
|   24  | ESRI             |                    |                    |
|   25  | Google Satellite |        10.232      |       8.930        |
|   25  | ESRI             |                    |                    |
|   26  | Google Satellite |        6.632       |       4.935        |
|   26  | ESRI             |                    |                    |
|   27  | Google Satellite |        38.489      |       17.570       |
|   27  | ESRI             |                    |                    |
|   28  | Google Satellite |        38.084      |       17.335       |
|   28  | ESRI             |                    |                    |
|   29  | Google Satellite |        20.144      |       10.309       |
|   29  | ESRI             |                    |                    |
|   30  | Google Satellite |        15.308      |       7.604        |
|   30  | ESRI             |                    |                    |
|   31  | Google Satellite |        22.122      |       10.063       |
|   31  | ESRI             |                    |                    |
|   32  | Google Satellite |        7.722       |       4.425        |
|   32  | ESRI             |                    |                    |
|   33  | Google Satellite |        17.858      |       8.183        |
|   33  | ESRI             |                    |                    |
|   34  | Google Satellite |        65.744      |       24.772       |
|   34  | ESRI             |                    |                    |
|   35  | Google Satellite |        10.183      |       7.592        |
|   35  | ESRI             |                    |                    |
|   36  | Google Satellite |        11.713      |       9.064        |
|   36  | ESRI             |                    |                    |
|   37  | Google Satellite |        26.921      |       16.238       |
|   37  | ESRI             |                    |                    |
|   38  | Google Satellite |        34.635      |      19.291        |
|   38  | ESRI             |                    |                    |
|   39  | Google Satellite |        114.422     |      141.640       |
|   39  | ESRI             |                    |                    |
|   40  | Google Satellite |        7.695       |      3.966         |
|   40  | ESRI             |                    |                    |
|   41  | Google Satellite |        11.585      |      6.862         |
|   41  | ESRI             |                    |                    |
|   42  | Google Satellite |        23.003      |      8.960         |
|   42  | ESRI             |                    |                    |
|   43  | Google Satellite |        30.533      |      14.345        |
|   43  | ESRI             |                    |                    |
|   44  | Google Satellite |        42.327      |       31.930       |
|   44  | ESRI             |                    |                    |