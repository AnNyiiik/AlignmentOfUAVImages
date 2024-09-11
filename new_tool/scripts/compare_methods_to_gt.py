import homography_finder_CNN_based
import homography_finder_feature_based
import util
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--paths_to_data", nargs="+", required=True)
parser.add_argument("--maps", nargs="+", required=True)
parser.add_argument(
    "--file_with_pair_names",
    type=str,
    help="file with names of aer and sat pics to align",
    required=True,
)
parser.add_argument(
    "--file_with_kpts_names",
    type=str,
    help="file with file names which contains gt correspondences",
    required=True,
)
parser.add_argument("--path_folder_to_save_results", type=str, required=True)
parser.add_argument("--draw_plot", type=bool, default=False)
parser.add_argument("--colors", nargs="+", default=["#faf75c"])

args = parser.parse_args()

homography_finder_feature = (
    homography_finder_feature_based.homography_finder_feature_based()
)
homography_finder_CNN = homography_finder_CNN_based.homography_finder_CNN_based()
data_for_plot = list()
plot_labels = list()

for path, map in zip(args.paths_to_data, args.maps):
    with open(os.path.join(path, args.file_with_pair_names), "r") as f:
        pair_names = f.readlines()

    with open(os.path.join(path, args.file_with_kpts_names), "r") as f:
        kpts_files = f.readlines()

    errors_feature, mean_feature, dev_feature = util.set_experiment(
        path, pair_names, kpts_files, homography_finder_feature, "feature method"
    )
    data_for_plot.append(errors_feature)
    plot_labels.append(f"feature +\n{map} map")

    errors_CNN, mean_CNN, dev_CNN = util.set_experiment(
        path, pair_names, kpts_files, homography_finder_CNN, "CNN method"
    )
    data_for_plot.append(errors_CNN)
    plot_labels.append(f"CNN +\n{map} map")

    util.save_experiment_results(
        args.path_folder_to_save_results,
        "feature",
        map,
        mean_feature,
        dev_feature,
        errors_feature,
    )
    util.save_experiment_results(
        args.path_folder_to_save_results, "CNN", map, mean_CNN, dev_CNN, errors_CNN
    )

if args.draw_plot:
    path_to_save_figure = str(
        os.path.join(
            args.path_folder_to_save_results, "reprojection_error_comparison.png"
        )
    )
    if len(args.colors) > 0:
        util.draw_box_plot(data_for_plot, path_to_save_figure, plot_labels, args.colors)
    else:
        util.draw_box_plot(data_for_plot, path_to_save_figure, plot_labels)
