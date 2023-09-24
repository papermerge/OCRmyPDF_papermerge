from pathlib import Path
from typing import List

from PIL import Image

from .utils import get_result_file_path


def generate_preview(
    input_file: Path,
    *,
    preview_width: int,
    base_dir: Path,
    uuids: List[str]
) -> None:
    """
    Generates page preview as jpeg
    """
    output_file_path = get_result_file_path(
        input_file_path=input_file,
        base_dir=base_dir,
        uuids=uuids,
        output_ext="jpg"
    )
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    im = Image.open(str(input_file))

    wpercent = (preview_width / float(im.size[0]))
    height = int((float(im.size[1]) * float(wpercent)))
    im = im.resize((preview_width, height), Image.LANCZOS)

    im.save(str(output_file_path), quality=50, format='JPEG')
