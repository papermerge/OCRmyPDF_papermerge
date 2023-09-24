from pathlib import Path

import pytest

from ocrmypdf_papermerge.utils import get_page_number, get_result_file_path


@pytest.mark.parametrize(
    'input_path,output_number',
    [
        (Path("/tmp/media/000001_ocr.jpeg"), 1),
        (Path("/tmp/media/000023_ocr.jpeg"), 23),
        (Path("/tmp/000003_ocr.png"), 3),
        (Path("/tmp/000005_ocr_hocr.hocr"), 5),
        (Path("/tmp/000005_ocr_hocr.txt"), 5),
        (Path("/tmp/asd.45.tmp/000005_ocr_hocr.txt"), 5),
        (Path("/tmp/asd.000123.tmp/000005_ocr_hocr.txt"), 5),
    ]
)
def test_get_page_number_positive_input(input_path, output_number):
    page_num_str = get_page_number(input_path)
    assert page_num_str == output_number


def test_get_page_number_negative_input():

    with pytest.raises(ValueError):
        get_page_number(10)  # noqa

    with pytest.raises(ValueError):
        # must be at least 6 characters long
        get_page_number("")  # noqa

    with pytest.raises(ValueError):
        # must be at least 6 characters long
        get_page_number("1234")  # noqa

    with pytest.raises(ValueError):
        # did not match
        get_page_number("_001.png")  # noqa


def test_get_result_file_path_positive_input():
    # all following calls use makedirs=False argument.
    # This way `get_result_file_path` will skip validation/creation of
    # missing folder
    output_file_path = get_result_file_path(
        input_file_path=Path("/tmp/media/000001_ocr.png"),
        base_dir=Path("/ocr/"),
        uuids=['8db234f4-9579-4dd8-86c9-2564d45de1ce'],
        output_ext="jpeg",
        makedirs=False
    )

    assert output_file_path == Path(
        "/ocr/8d/b2/8db234f4-9579-4dd8-86c9-2564d45de1ce/page.jpeg"
    )

    output_file_path = get_result_file_path(
        input_file_path=Path("/tmp/000002_ocr.png"),
        base_dir=Path("/media/"),
        uuids=[
            '8db234f4-9579-4dd8-86c9-2564d45de1ce',
            'ed06dc8c-6675-47d4-ad41-1edb8c43030c'  # UUID for the second page
        ],
        output_ext="txt",
        makedirs=False
    )

    expected = Path(
        "/media/ed/06/ed06dc8c-6675-47d4-ad41-1edb8c43030c/page.txt"
    )
    assert output_file_path == expected
