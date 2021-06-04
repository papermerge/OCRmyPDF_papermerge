import os
import re
import shutil


def get_page_number(input_file_path):
    """
    Given input_file_path it returns page number as string.

    e.g.:

    "/tmp/media/000001_ocr.jpeg" => "000001"
    "/tmp/media/000022_ocr.txt" => "000022"
    """
    if not isinstance(input_file_path, str):
        raise ValueError("Expecting a string as input")

    if len(input_file_path) < 6:  # page number has 6 digits
        raise ValueError("Expecting a string at least 6 characters long")

    PATTERN = r"(?P<page_num>\d{6})"
    match = re.search(PATTERN, input_file_path)
    if match:
        return match.group('page_num')

    # always should match, otherwise there is something wrong
    # with input. Maybe OCRmyPDF output format changed?
    raise ValueError("get_page_number did not match")


def get_result_file_path(
    input_file_path,
    output_dir,
    output_ext,
    makedirs=True
):
    """
    Example 1:

    input:
        input_file_path: "/tmp/media/000001_ocr.png"
        output_dir: "/ocr/user_1/pages"
        output_ext: "jpeg"

    output:
        "/ocr/user_1/pages/000001/000001_ocr.jpeg"
    Plus it makes sure folder /ocr/user_1/pages/000001/ exists
    and if not - it creates it.

    Example 2:

    input:
        input_file_path: "/tmp/000023_ocr.png"
        output_dir: "/media/results/user_1/pages"
        output_ext: "txt"

    output:
        "/media/results/user_1/pages/000023/000023_ocr.txt"
    Plus it makes sure folder /media/results/user_1/pages/000023/ exists
    and if not - it creates it.
    """
    page_number_str = get_page_number(input_file_path)
    basename = os.path.basename(input_file_path)
    root, _ = os.path.splitext(basename)

    result_dir_path = os.path.join(
        output_dir, page_number_str
    )
    if makedirs:  # during unittesting makedirs=False
        if not os.path.exists(result_dir_path):
            os.makedirs(
                result_dir_path,
                exist_ok=True
            )

    return f"{result_dir_path}/{root}.{output_ext}"


def copy_txt(
    input_file_path,
    output_dir
):
    output_file_path = get_result_file_path(
        input_file_path=input_file_path,
        output_dir=output_dir,
        output_ext="txt"
    )
    shutil.copy(input_file_path, output_file_path)


def copy_hocr(
    input_file_path,
    output_dir
):
    output_file_path = get_result_file_path(
        input_file_path=input_file_path,
        output_dir=output_dir,
        output_ext="hocr"
    )
    shutil.copy(input_file_path, output_file_path)
