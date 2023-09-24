from pathlib import Path

from PIL import Image

from .utils import get_result_file_path


def generate_preview(
    input_file: Path | str,
    preview_width: int,
    sidecar_dir: Path | str
) -> None:
    """
    Generates page preview as jpeg
    """
    output_file_path = get_result_file_path(
        input_file_path=str(input_file),
        base_dir=str(sidecar_dir),
        output_ext="jpg"
    )

    im = Image.open(input_file)

    wpercent = (preview_width / float(im.size[0]))
    height = int((float(im.size[1]) * float(wpercent)))
    im = im.resize((preview_width, height), Image.LANCZOS)

    im.save(output_file_path, quality=50, format='JPEG')
