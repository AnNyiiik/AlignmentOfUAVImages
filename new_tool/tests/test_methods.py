import pytest
import numpy as np
import os

from scripts import homography_finder_feature_based
from scripts import homography_finder_CNN_based


homography_finder_feature = (
    homography_finder_feature_based.homography_finder_feature_based()
)
homography_finder_CNN = homography_finder_CNN_based.homography_finder_CNN_based()

testdata_homography_search = [
    (
        homography_finder_feature,
        os.path.abspath("tests/exp_data/aer_1.png"),
        os.path.abspath("tests/exp_data/sat_1.png"),
    ),
    (
        homography_finder_CNN,
        os.path.abspath("tests/exp_data/aer_1.png"),
        os.path.abspath("tests/exp_data/sat_1.png"),
    ),
]


@pytest.mark.parametrize("method,query_path,reference_path", testdata_homography_search)
def test_check_homography_search(method, query_path, reference_path):
    H = method.align(query_path, reference_path)
    assert type(H) == np.ndarray
    assert H.shape == (3, 3)


testdata_bad_input = [
    (
        homography_finder_feature,
        os.path.abspath("tests/exp_data/aer_2.png"),
        os.path.abspath("tests/exp_data/sat_3.png"),
    ),
    (
        homography_finder_CNN,
        os.path.abspath("tests/exp_data/aer_2.png"),
        os.path.abspath("tests/exp_data/sat_3.png"),
    ),
    (
        homography_finder_feature,
        os.path.abspath("tests/exp_data/aer_3.png"),
        os.path.abspath("tests/exp_data/sat_2.png"),
    ),
    (
        homography_finder_CNN,
        os.path.abspath("tests/exp_data/aer_3.png"),
        os.path.abspath("tests/exp_data/sat_2.png"),
    ),
]


@pytest.mark.parametrize("method,query_path,reference_path", testdata_bad_input)
def test_check_bad_user_input(method, query_path, reference_path):
    with pytest.raises(FileNotFoundError):
        method.align(query_path, reference_path)
