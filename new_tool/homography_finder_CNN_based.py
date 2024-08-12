import docker
import os
from pathlib import Path

import util
import homography_finder
import homography_finder_feature_based

class homography_finder_CNN_based(homography_finder.homography_finder):

    def align(self, img_query_path, img_reference_path):
        img_query_cropped = util.clip_image(img_query_path)
        height, width, _ = img_query_cropped.shape
        img_reference_cropped = util.clip_image(img_reference_path)

        query_saved_path, reference_saved_path = \
            util.create_temporary_folders_for_images(img_query_cropped, img_reference_cropped)

        H = homography_finder_feature_based.homography_finder_feature_based().align(img_query_path, img_reference_path)[0]

        client = docker.from_env()
        if (len(list(filter(lambda container: container.name == "CNN_method", client.containers.list(all=True)))) == 0):
            image_id = client.images.get("anyaaaaaa/unsupervised_deep_homography:version_4").id
            os.system(f'docker container create -it --name CNN_method {image_id}')
            path_to_model = Path('~/real_models').expanduser()
            container_id = util.get_container_id_by_name(client, "CNN_method")
            os.system(
                f'docker cp {path_to_model} {container_id}:/workspace/unsupervisedDeepHomographyRAL2018/models')

        container_id = util.get_container_id_by_name(client, "CNN_method")
        os.system(f'docker container start {container_id}')

        path_to_data_inside_container = f'{container_id}:/workspace/unsupervisedDeepHomographyRAL2018/data'
        os.system(f'docker cp {query_saved_path} {path_to_data_inside_container}/query.jpg')
        os.system(f'docker cp {reference_saved_path} {path_to_data_inside_container}/reference.jpg')

        images_names_path, gt_path, query_corners_path = util.make_data_for_CNN_method(width, height, H)

        path_to_save = f'{path_to_data_inside_container}/test_real.txt'
        os.system(f'docker cp {images_names_path} {path_to_save}')

        path_to_save = f'{path_to_data_inside_container}/test_gt.txt'
        os.system(f'docker cp {gt_path} {path_to_save}')

        path_to_save = f'{path_to_data_inside_container}/test_pts1.txt'
        os.system(f'docker cp {query_corners_path} {path_to_save}')

        absolute_path = Path('~/AlignmentOfUAVImages').expanduser()
        path_to_save_result_matrix = str(absolute_path.joinpath("CNN_result.txt"))
        os.system(f'docker exec {container_id} python code/homography_CNN_real.py --mode=test --batch_size=2')
        os.system(f'docker cp {container_id}:/workspace/log/results/homographies.txt {path_to_save_result_matrix}')
        os.system(f'docker stop {container_id}')
        H = util.read_homography_matrix_from_file(path_to_save_result_matrix)
        return H