import base64
import os.path
from PIL import Image
from io import BytesIO


SVG_TEMPLATE = """
<svg viewBox="0 0 2480 3495" xmlns="http://www.w3.org/2000/svg">
  <image
    width="2480"
    href="data:image/jpeg;base64,{base64_img}"
    />
</svg>
"""


def image_to_base64(image_path):
    im = Image.open(image_path)
    rgb_im = im.convert('RGB')
    output_buffer = BytesIO()
    # f"{options.svg_output_folder}/{root}.jpg"
    rgb_im.save(output_buffer, quality=50, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)

    return base64_str


def generate_svg(input_file, input_hocr, options):
    """
    Generates page SVG with embedded raster image and text overlay.
    """
    basename = os.path.basename(input_file)
    root, _ = os.path.splitext(basename)
    base64_img = image_to_base64(input_file)
    svg_file_path = f"{options.svg_output_folder}/{root}.svg"

    with open(svg_file_path, 'wt') as f:
        f.write(SVG_TEMPLATE.format(base64_img=base64_img.decode('utf-8')))

    print(
        f"GENERATE_SVG: input_file: {input_file}, input_hocr: {input_hocr}"
    )
