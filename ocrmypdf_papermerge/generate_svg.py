from .hocr import get_words
from .image import image_to_base64
from .render import render_to_string
from .utils import get_result_file_path


def generate_svg(input_file, input_hocr, options):
    """
    Generates page SVG with embedded raster image and text overlay.
    """
    output_file_path = get_result_file_path(
        input_file_path=str(input_file),
        output_dir=options.sidecar_dir,
        output_ext=options.sidecar_format
    )

    base64_img, size = image_to_base64(input_file)

    words = get_words(input_hocr)

    output_format = options.sidecar_format  # svg | html
    template_name = f"page.{output_format}.j2"  # svg | html

    rendered_string = render_to_string(
        template_name,
        base64_img=base64_img.decode('utf-8'),
        width=size[0],
        height=size[1],
        words=words
    )

    with open(output_file_path, 'wt') as f:
        f.write(rendered_string)
