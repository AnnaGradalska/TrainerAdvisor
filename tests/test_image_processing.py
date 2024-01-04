import unittest
import cv2
import numpy as np
from src.core.image_processing_tools.image_processing import draw_points, sort_points


class TestImageProcessing(unittest.TestCase):
    def test_draw_points_with_dots(self):
        image_with_dots = np.zeros((700, 400, 3), dtype=np.uint8)

        dots_coordinates = [(200, 220), (250, 270), (300, 320), (250, 370), (300, 420),
                            (200, 470), (250, 520), (300, 570), (250, 620), (300, 670), (250, 720)]

        for coord in dots_coordinates:
            if 0 <= coord[1] < 700 and 0 <= coord[0] < 400:
                cv2.circle(image_with_dots, coord, radius=5, color=[255, 255, 255], thickness=-1)

        gray_image_with_dots = cv2.cvtColor(image_with_dots, cv2.COLOR_BGR2GRAY)
        sorted_points, _ = draw_points(gray_image_with_dots, 0)

        self.assertEqual(len(sorted_points), 11)

    def test_draw_points_without_dots(self):
        image_without_dots = np.zeros((700, 400, 3), dtype=np.uint8)
        gray_image_with_dots = cv2.cvtColor(image_without_dots, cv2.COLOR_BGR2GRAY)
        sorted_points, _ = draw_points(gray_image_with_dots, 0)

        self.assertEqual(len(sorted_points), 0)

    def test_sort_points_basic(self):
        centers = [(10, 20), (30, 40), (15, 25), (25, 35), (5, 15)]
        sorted_points = sort_points(centers)
        expected_result = [(5, 15), (10, 20), (15, 25), (25, 35), (30, 40)]
        self.assertEqual(sorted_points, expected_result)

    def test_sort_points_ignore_positions(self):
        centers = [(165, 508), (256, 503), (154, 438), (261, 433), (170, 362), (243, 357), (207, 343), (140, 301),
                   (267, 293), (177, 263), (230, 262), (204, 255)]
        sorted_points = sort_points(centers)
        expected_result = [(204, 255), (177, 263), (230, 262), (140, 301), (267, 293), (207, 343), (170, 362),
                           (243, 357), (154, 438), (261, 433), (165, 508), (256, 503)]
        self.assertEqual(sorted_points, expected_result)


if __name__ == '__main__':
    unittest.main()
