import docker
import os
import shutil

from pathlib import Path
from scripts import util
from scripts import homography_finder
from scripts import homography_finder_feature_based


class homography_finder_CNN_based(homography_finder.homography_finder):
    def align(self, img_query_path, img_reference_path):
        if not os.path.exists(os.path.abspath(img_query_path)):
            raise FileNotFoundError(f"file {img_query_path} does not exist")
        elif not os.path.exists(os.path.abspath(img_reference_path)):
            raise FileNotFoundError(f"file {img_reference_path} does not exist")

        img_query_cropped = util.clip_image(img_query_path)
        height, width, _ = img_query_cropped.shape
        img_reference_cropped = util.clip_image(img_reference_path)

        absolute_path = Path("~/AlignmentOfUAVImages").expanduser()

        (
            query_saved_path,
            reference_saved_path,
        ) = util.create_temporary_folders_for_images(
            img_query_cropped,
            img_reference_cropped,
            os.path.join(absolute_path, "CNN_method_images"),
        )

        H = homography_finder_feature_based.homography_finder_feature_based().align(
            img_query_path, img_reference_path
        )

        client = docker.from_env()
        if len(client.images.get("anyaaaaaa/unsupervised_deep_homography:version_4")) == 0:
            os.system('docker pull anyaaaaaa/unsupervised_deep_homography:version_4')
        if (
            len(
                list(
                    filter(
                        lambda container: container.name == "CNN_method",
                        client.containers.list(all=True),
                    )
                )
            )
            == 0
        ):
            image_id = client.images.get(
                "anyaaaaaa/unsupervised_deep_homography:version_4"
            ).id
            os.system(f"docker container create -it --name CNN_method {image_id}")
            path_to_model = os.path.abspath("real_models")
            container_id = util.get_container_id_by_name(client, "CNN_method")
            os.system(
                f"docker cp {path_to_model} {container_id}:/workspace/unsupervisedDeepHomographyRAL2018/models >/dev/null 2>&1"
            )

        container_id = util.get_container_id_by_name(client, "CNN_method")
        os.system(f"docker container start {container_id} >/dev/null 2>&1")

        path_to_data_inside_container = (
            f"{container_id}:/workspace/unsupervisedDeepHomographyRAL2018/data"
        )
        os.system(
            f"docker cp {query_saved_path} {path_to_data_inside_container}/query.jpg >/dev/null 2>&1"
        )
        os.system(
            f"docker cp {reference_saved_path} {path_to_data_inside_container}/reference.jpg >/dev/null 2>&1"
        )

        (
            images_names_path,
            gt_path,
            query_corners_path,
            path_to_CNN_data,
        ) = util.make_data_for_CNN_method(width, height, H)

        path_to_save = f"{path_to_data_inside_container}/test_real.txt"
        os.system(f"docker cp {images_names_path} {path_to_save} >/dev/null 2>&1")

        path_to_save = f"{path_to_data_inside_container}/test_gt.txt"
        os.system(f"docker cp {gt_path} {path_to_save} >/dev/null 2>&1")

        path_to_save = f"{path_to_data_inside_container}/test_pts1.txt"
        os.system(f"docker cp {query_corners_path} {path_to_save} >/dev/null 2>&1")

        path_to_save_result_matrix = str(os.path.join(absolute_path, "CNN_result.txt"))
        os.system(
            f"docker exec {container_id} python code/homography_CNN_real.py --mode=test --batch_size=2 >/dev/null 2>&1"
        )
        os.system(
            f"docker cp {container_id}:/workspace/log/results/homographies.txt {path_to_save_result_matrix} >/dev/null 2>&1"
        )
        os.system(f"docker stop {container_id} >/dev/null 2>&1")

        H = util.read_homography_matrix_from_file(path_to_save_result_matrix)
        shutil.rmtree(os.path.join(absolute_path, "CNN_method_images"))
        shutil.rmtree(path_to_CNN_data)
        os.remove(path_to_save_result_matrix)
        return H
