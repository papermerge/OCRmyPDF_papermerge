import os
from pathlib import Path

import pytest

from ocrmypdf_papermerge.generate_preview import generate_preview

TEST_DATA_FOLDER = Path(os.path.dirname(__file__)) / 'data'


@pytest.mark.parametrize(
    "test_input, uuid, expected_file_path",
    [
        (
            "000001_ocr.jpg",
            '75d61315-a12d-4860-97d3-431f395e82f4',
            Path("75/d6/75d61315-a12d-4860-97d3-431f395e82f4/page.jpg")
        ),
        (
            "000002.jpg",
            '532a4ec9-0405-44d8-be0c-ebb33944c427',
            Path("53/2a/532a4ec9-0405-44d8-be0c-ebb33944c427/page.jpg")
        ),
        (
            "000002_ocr.jpeg",
            '14bdc2b4-3923-44c2-b62a-a00afc2e1bc7',
            Path("14/bd/14bdc2b4-3923-44c2-b62a-a00afc2e1bc7/page.jpg")
        )
    ]
)
def test_generate_preview(
    tmp_path,
    test_input,
    uuid,
    expected_file_path
):
    base_dir = tmp_path / "media_root" / "ocr"
    base_dir.mkdir(parents=True, exist_ok=True)

    generate_preview(
        TEST_DATA_FOLDER / test_input,
        preview_width=100,
        base_dir=base_dir,
        uuid=uuid
    )

    expected_path = Path(base_dir / expected_file_path)

    assert expected_path.exists()


def test_generate_preview_will_raise_exp_on_invalid_file_name(tmp_path: Path):
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

    with pytest.raises(FileNotFoundError):
        generate_preview(
            input_file=TEST_DATA_FOLDER / '01_ocr.jpg',
            preview_width=100,
            uuid='',
            base_dir=sidecar_dir
        )

    with pytest.raises(FileNotFoundError):
        generate_preview(
            input_file=TEST_DATA_FOLDER / '99.jpg',
            preview_width=100,
            uuid='',
            base_dir=sidecar_dir
        )
