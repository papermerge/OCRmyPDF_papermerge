import os
import re
import shutil
from pathlib import Path
from typing import List


def get_page_number(input_file_path: Path) -> int:
    """
    Given input_file_path it returns page number as integer.

    e.g.:

    Path("/tmp/media/000001_ocr.jpeg") => 1
    Path("/tmp/media/000022_ocr.txt") => 22
    """
    if not isinstance(input_file_path, (Path, str)):
        raise ValueError("Expecting Path or str instance as input")

    if len(str(input_file_path)) < 6:
        raise ValueError("Expecting path to be at least 6 chars long")

    PATTERN = r"\/(?P<page_num>\d{6})"

    match = re.search(PATTERN, str(input_file_path))
    if match:
        result = match.group('page_num')
        return int(result.lstrip("0"))

    # always should match, otherwise there is something wrong
    # with input. Maybe OCRmyPDF output format changed?
    raise ValueError(f"Input {input_file_path} did not match expected pattern.")


def get_result_file_path(
    input_file_path: Path,
    *,
    base_dir: Path,
    uuids: List[str],
    output_ext,
    makedirs=True
) -> Path:
    """
    Example 1:

    input:
        input_file_path: Path('/tmp/media/000001_ocr.png')
        base_dir: Path('/ocr/')
        uuids: ['8db234f4-9579-4dd8-86c9-2564d45de1ce']
        output_ext: 'jpeg'

    output:
        Path('/ocr/8d/b2/8db234f4-9579-4dd8-86c9-2564d45de1ce/page.jpeg')

    Example 2:

    input:
        input_file_path: Path('/tmp/000023_ocr.png')
        base_dir: Path('/ocr')
        uuids: [...22 more uuids...,'a5b93d53-d62b-4264-a368-8122a8c313bc']
        output_ext: 'txt'

    output:
        Path('/ocr/a5/b9/a5b93d53-d62b-4264-a368-8122a8c313bc/page.txt')
    """
    page_number = get_page_number(input_file_path)

    if page_number > len(uuids):
        raise ValueError(
            f"page_number > len(uuids) i.e. {page_number} > {len(uuids)}"
        )

    uuid = uuids[page_number - 1]
    basename = os.path.basename(input_file_path)
    root, _ = os.path.splitext(basename)

    result_dir_path = Path(
        base_dir, uuid[0:2], uuid[2:4], uuid
    )

    if makedirs:  # during unit testing makedirs=False
        if result_dir_path.exists():
            os.makedirs(
                result_dir_path,
                exist_ok=True
            )

    return Path(result_dir_path, f"page.{output_ext}")


def copy_txt(
    input_file_path: Path,
    output_dir: Path,
    uuids: List[str]
):
    output_file_path = get_result_file_path(
        input_file_path,
        base_dir=output_dir,
        output_ext="txt",
        uuids=uuids
    )
    shutil.copy(input_file_path, output_file_path)


def copy_hocr(
    input_file_path: Path,
    output_dir: Path,
    uuids: List[str]
):
    output_file_path = get_result_file_path(
        input_file_path,
        base_dir=output_dir,
        output_ext="hocr",
        uuids=uuids
    )
    shutil.copy(input_file_path, output_file_path)
