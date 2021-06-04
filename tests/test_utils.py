import unittest

from ocrmypdf_papermerge.utils import (
    get_page_number,
    get_result_file_path
)


class TestUtils(unittest.TestCase):

    def test_get_page_number_positive_input(self):

        page_num_str = get_page_number("/tmp/media/000001_ocr.jpeg")
        self.assertEqual(page_num_str, "000001")

        page_num_str = get_page_number("/tmp/000023_ocr.jpeg")
        self.assertEqual(page_num_str, "000023")

        page_num_str = get_page_number("/tmp/000003_ocr.png")
        self.assertEqual(page_num_str, "000003")

        page_num_str = get_page_number("/tmp/000005_ocr_hocr.hocr")
        self.assertEqual(page_num_str, "000005")

        page_num_str = get_page_number("/tmp/000005_ocr_hocr.txt")
        self.assertEqual(page_num_str, "000005")

    def test_get_page_number_negative_input(self):

        with self.assertRaises(ValueError):
            get_page_number(10)

        with self.assertRaises(ValueError):
            # must be at least 6 characters long
            get_page_number("")

        with self.assertRaises(ValueError):
            # must be at least 6 characters long
            get_page_number("1234")

        with self.assertRaises(ValueError):
            # did not match
            get_page_number("_001.png")

    def test_get_result_file_path_positive_input(self):

        # all following calls use makedirs=False argument.
        # This way `get_result_file_path` will skip validation/creation of
        # missing folder
        output_file_path = get_result_file_path(
            input_file_path="/tmp/media/000001_ocr.png",
            output_dir="/ocr/user_1/pages",
            output_ext="jpeg",
            makedirs=False
        )

        self.assertEqual(
            output_file_path,
            "/ocr/user_1/pages/000001/000001_ocr.jpeg"
        )

        output_file_path = get_result_file_path(
            input_file_path="/tmp/000023_ocr.png",
            output_dir="/media/results/user_1/pages",
            output_ext="txt",
            makedirs=False
        )

        self.assertEqual(
            output_file_path,
            "/media/results/user_1/pages/000023/000023_ocr.txt"
        )
