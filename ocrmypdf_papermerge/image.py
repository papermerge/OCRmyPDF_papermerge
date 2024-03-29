import base64
from io import BytesIO
from pathlib import Path

from PIL import Image


def image_to_base64(image_path: Path) -> [str, [int, int]]:
    """
    Converts image to base64 encoded string.

    image_path: path to input image

    Returns 2 values tuple:
        1. encoded base64 string (str)
        2. size tuple with:
            a. width (int)
            b. height (int)
    """
    im = Image.open(str(image_path))
    rgb_im = im.convert('RGB')
    output_buffer = BytesIO()
    # f"{options.svg_output_folder}/{root}.jpg"
    rgb_im.save(output_buffer, quality=50, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)

    return base64_str, rgb_im.size
