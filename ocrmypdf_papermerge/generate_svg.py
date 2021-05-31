import os.path

from .hocr import get_words
from .image import image_to_base64
from .render import render_to_string


def generate_svg(input_file, input_hocr, options):
    """
    Generates page SVG with embedded raster image and text overlay.
    """
    basename = os.path.basename(input_file)
    root, _ = os.path.splitext(basename)

    base64_img, size = image_to_base64(input_file)

    words = get_words(input_hocr)

    svg_file_path = f"{options.svg_output_folder}/{root}.svg"
    svg_file_output = render_to_string(
        "templates/page.svg.j2",
        base64_img=base64_img.decode('utf-8'),
        width=size[0],
        height=size[1],
        words=words
    )

    with open(svg_file_path, 'wt') as f:
        f.write(svg_file_output)
