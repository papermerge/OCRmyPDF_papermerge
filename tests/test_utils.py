import pytest

from ocrmypdf_papermerge.utils import (
    get_page_number,
    get_result_file_path
)


def test_get_page_number_positive_input():

    page_num_str = get_page_number("/tmp/media/000001_ocr.jpeg")
    assert page_num_str == "000001"

    page_num_str = get_page_number("/tmp/000023_ocr.jpeg")
    assert page_num_str == "000023"

    page_num_str = get_page_number("/tmp/000003_ocr.png")
    assert page_num_str == "000003"

    page_num_str = get_page_number("/tmp/000005_ocr_hocr.hocr")
    assert page_num_str == "000005"

    page_num_str = get_page_number("/tmp/000005_ocr_hocr.txt")
    assert page_num_str == "000005"


def test_get_page_number_negative_input():

    with pytest.raises(ValueError):
        get_page_number(10)

    with pytest.raises(ValueError):
        # must be at least 6 characters long
        get_page_number("")

    with pytest.raises(ValueError):
        # must be at least 6 characters long
        get_page_number("1234")

    with pytest.raises(ValueError):
        # did not match
        get_page_number("_001.png")


def test_get_result_file_path_positive_input():

    # all following calls use makedirs=False argument.
    # This way `get_result_file_path` will skip validation/creation of
    # missing folder
    output_file_path = get_result_file_path(
        input_file_path="/tmp/media/000001_ocr.png",
        output_dir="/ocr/user_1/pages",
        output_ext="jpeg",
        makedirs=False
    )

    assert output_file_path == "/ocr/user_1/pages/000001/000001_ocr.jpeg"

    output_file_path = get_result_file_path(
        input_file_path="/tmp/000023_ocr.png",
        output_dir="/media/results/user_1/pages",
        output_ext="txt",
        makedirs=False
    )

    expected_str = "/media/results/user_1/pages/000023/000023_ocr.txt"
    assert output_file_path == expected_str
