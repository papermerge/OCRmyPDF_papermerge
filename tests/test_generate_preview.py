import os
from pathlib import Path

import pytest

from ocrmypdf_papermerge.generate_preview import generate_preview

TEST_DATA_FOLDER = Path(os.path.dirname(__file__)) / 'data'


@pytest.mark.parametrize(
    "test_input, expected_sidecar, expected_filename",
    [
        ("000001_ocr.jpg", "000001", "000001_ocr.jpg"),
        ("000999.jpg", "000999", "000999.jpg"),
        ("000999_ocr.jpeg", "000999", "000999_ocr.jpg"),
    ]
)
def test_generate_preview(
    tmp_path: Path,
    test_input,
    expected_sidecar,
    expected_filename
):
    sidecar_dir = tmp_path / "sidecar_dir"
    sidecar_dir.mkdir()

    generate_preview(
        input_file=TEST_DATA_FOLDER / test_input,
        preview_width=100,
        sidecar_dir=sidecar_dir
    )

    expected_path = Path(sidecar_dir / expected_sidecar / expected_filename)
    assert expected_path.exists()


def test_generate_preview_will_raise_exception_on_invalid_file_name(tmp_path: Path):
    """input file basename should contain 6 character page number

    Correct image basenames:
        000120_ocr.jpg -> page number 120
        000009_ocr.jpg -> page number 9
        000999.jpg -> page number 999

    Wrong image basenames:
        01_ocr.jpg -> page number has only 2 characters
        9.jpg -> page number has only 1 character
    """
    sidecar_dir = tmp_path / "sidecar_dir"
    sidecar_dir.mkdir()

    with pytest.raises(ValueError):
        generate_preview(
            input_file=TEST_DATA_FOLDER / '01_ocr.jpg',
            preview_width=100,
            sidecar_dir=sidecar_dir
        )

    with pytest.raises(ValueError):
        generate_preview(
            input_file=TEST_DATA_FOLDER / '99.jpg',
            preview_width=100,
            sidecar_dir=sidecar_dir
        )
