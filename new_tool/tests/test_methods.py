import unittest
from unittest import TestCase
import numpy as np
import os

from parameterized import parameterized, parameterized_class

from scripts import homography_finder_feature_based
from scripts import homography_finder_CNN_based


class TestClass(TestCase):
    homography_finder_feature = (
        homography_finder_feature_based.homography_finder_feature_based()
    )
    homography_finder_CNN = homography_finder_CNN_based.homography_finder_CNN_based()

    @parameterized.expand(
        [
            (
                homography_finder_feature,
                os.path.abspath("exp_data/aer_1.png"),
                os.path.abspath("exp_data/sat_1.png"),
            ),
            (
                homography_finder_CNN,
                os.path.abspath("exp_data/aer_1.png"),
                os.path.abspath("exp_data/sat_1.png"),
            ),
        ]
    )
    def test_check_homography_search(self, method, query_path, reference_path):
        H = method.align(query_path, reference_path)
        assert type(H) == np.ndarray
        assert H.shape == (3, 3)

    @parameterized.expand(
        [
            (
                homography_finder_feature,
                os.path.abspath("exp_data/aer_2.png"),
                os.path.abspath("exp_data/sat_3.png"),
            ),
            (
                homography_finder_CNN,
                os.path.abspath("exp_data/aer_2.png"),
                os.path.abspath("exp_data/sat_3.png"),
            ),
            (
                homography_finder_feature,
                os.path.abspath("exp_data/aer_3.png"),
                os.path.abspath("exp_data/sat_2.png"),
            ),
            (
                homography_finder_CNN,
                os.path.abspath("exp_data/aer_3.png"),
                os.path.abspath("exp_data/sat_2.png"),
            ),
        ]
    )
    def test_check_bad_user_input(self, method, query_path, reference_path):
        with self.assertRaises(FileNotFoundError):
            method.align(query_path, reference_path)


if __name__ == "__main__":
    unittest.main()
