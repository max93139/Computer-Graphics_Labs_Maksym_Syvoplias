# -*- coding: utf-8 -*-
"""
Набір автоматизованих тестів для перевірки алгоритмів Лабораторної роботи №6.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.
"""

import os
import sys
import unittest
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import lab6_manual_algorithms as algos
import lab6_operations as ops


class TestLab6ManualAlgorithms(unittest.TestCase):

    def setUp(self):
        self.black_3x3 = [(0, 0, 0)] * 9
        self.white_3x3 = [(255, 255, 255)] * 9
        self.gradient_3x3 = [
            (10, 10, 10), (20, 20, 20), (30, 30, 30),
            (40, 40, 40), (50, 50, 50), (60, 60, 60),
            (70, 70, 70), (80, 80, 80), (90, 90, 90)
        ]

    def test_clamp_val(self):
        self.assertEqual(algos.clamp_val(-10), 0)
        self.assertEqual(algos.clamp_val(300), 255)
        self.assertEqual(algos.clamp_val(127.4), 127)
        self.assertEqual(algos.clamp_val(127.6), 128)

    def test_calculate_luminance(self):
        lum_white = algos.calculate_luminance(255, 255, 255)
        self.assertAlmostEqual(lum_white, 255.0, places=2)
        lum_black = algos.calculate_luminance(0, 0, 0)
        self.assertAlmostEqual(lum_black, 0.0, places=2)

    def test_uniform_invariance_linear_filters(self):
        kernels = [
            algos.get_box_filter_kernel(3),
            algos.get_box_filter_kernel(5),
            algos.get_gaussian_3x3_kernel(),
            algos.get_gaussian_5x5_kernel(),
        ]
        for kernel in kernels:
            filtered_black = algos.apply_linear_filter(self.black_3x3, 3, 3, kernel)
            self.assertEqual(filtered_black, self.black_3x3)
            filtered_white = algos.apply_linear_filter(self.white_3x3, 3, 3, kernel)
            self.assertEqual(filtered_white, self.white_3x3)

    def test_uniform_invariance_nonlinear_filters(self):
        filters = [
            lambda p: algos.apply_median_filter(p, 3, 3, radius=1),
            lambda p: algos.apply_median_filter(p, 3, 3, radius=2),
            lambda p: algos.apply_min_filter(p, 3, 3, radius=1),
            lambda p: algos.apply_max_filter(p, 3, 3, radius=1),
            lambda p: algos.apply_midpoint_filter(p, 3, 3, radius=1),
            lambda p: algos.apply_alpha_trimmed_mean_filter(p, 3, 3, radius=1, d=4),
            lambda p: algos.apply_adaptive_median_filter(p, 3, 3, max_radius=2),
        ]
        for f in filters:
            self.assertEqual(f(self.black_3x3), self.black_3x3)
            self.assertEqual(f(self.white_3x3), self.white_3x3)

    def test_impulse_suppression_median(self):
        impulse_array = [(0, 0, 0)] * 9
        impulse_array[4] = (255, 255, 255)
        filtered = algos.apply_median_filter(impulse_array, 3, 3, radius=1)
        self.assertEqual(filtered[4], (0, 0, 0))

    def test_alpha_channel_preservation(self):
        rgba_array = [(100, 150, 200, 128)] * 9
        filtered = algos.apply_linear_filter(rgba_array, 3, 3, algos.get_box_filter_kernel(3))
        for p in filtered:
            self.assertEqual(len(p), 4)
            self.assertEqual(p[3], 128)

        filtered_med = algos.apply_median_filter(rgba_array, 3, 3, radius=1)
        for p in filtered_med:
            self.assertEqual(len(p), 4)
            self.assertEqual(p[3], 128)

    def test_empty_input_graceful_handling(self):
        empty_px = []
        self.assertEqual(algos.add_gaussian_noise(empty_px, 0, 0), [])
        self.assertEqual(algos.add_impulse_noise(empty_px, 0, 0), [])
        self.assertEqual(algos.add_brightness_dependent_noise(empty_px, 0, 0), [])
        self.assertEqual(algos.add_spatial_coordinate_noise(empty_px, 0, 0), [])
        self.assertEqual(algos.apply_linear_filter(empty_px, 0, 0, algos.get_box_filter_kernel(3)), [])
        self.assertEqual(algos.apply_median_filter(empty_px, 0, 0, 1), [])
        self.assertEqual(algos.apply_min_filter(empty_px, 0, 0, 1), [])
        self.assertEqual(algos.apply_max_filter(empty_px, 0, 0, 1), [])
        self.assertEqual(algos.apply_midpoint_filter(empty_px, 0, 0, 1), [])
        self.assertEqual(algos.apply_alpha_trimmed_mean_filter(empty_px, 0, 0, 1, 4), [])
        self.assertEqual(algos.apply_adaptive_median_filter(empty_px, 0, 0, 2), [])
        self.assertEqual(algos.calculate_mse([], []), 0.0)
        self.assertEqual(algos.calculate_psnr([], []), 99.99)

    def test_non_square_dimensions(self):
        px_5x1 = [(i * 20, i * 20, i * 20) for i in range(5)]
        res_linear = algos.apply_linear_filter(px_5x1, 5, 1, algos.get_box_filter_kernel(3))
        self.assertEqual(len(res_linear), 5)

        px_1x5 = [(i * 30, i * 30, i * 30) for i in range(5)]
        res_med = algos.apply_median_filter(px_1x5, 1, 5, radius=1)
        self.assertEqual(len(res_med), 5)

    def test_metrics_accuracy(self):
        img_a = [(100, 100, 100)] * 10
        img_b = [(110, 110, 110)] * 10
        mse = algos.calculate_mse(img_a, img_b)
        self.assertAlmostEqual(mse, 100.0, places=2)

        psnr = algos.calculate_psnr(img_a, img_b)
        expected_psnr = 10.0 * math.log10((255.0 ** 2) / 100.0)
        self.assertAlmostEqual(psnr, expected_psnr, places=2)

        self.assertAlmostEqual(algos.calculate_distortion(img_a, img_b), 100.0, places=2)
        self.assertEqual(algos.calculate_psnr(img_a, img_a), 99.99)

    def test_filter_requirements_coverage(self):
        linear_count = sum(1 for _, f_type, _ in ops.AVAILABLE_FILTERS if f_type == "linear")
        nonlinear_count = sum(1 for _, f_type, _ in ops.AVAILABLE_FILTERS if f_type == "non-linear")
        self.assertGreaterEqual(linear_count, 3, "Повинно бути не менше 3 лінійних фільтрів")
        self.assertGreaterEqual(nonlinear_count, 7, "Повинно бути не менше 7 нелінійних фільтрів")


if __name__ == '__main__':
    unittest.main()
