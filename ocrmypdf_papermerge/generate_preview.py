from PIL import Image

from .utils import get_result_file_path


def generate_preview(input_file, options):
    """
    Generates page preview as jpeg
    """
    output_file_path = get_result_file_path(
        input_file_path=str(input_file),
        output_dir=options.sidecar_dir,
        output_ext="jpg"
    )

    im = Image.open(input_file)

    width = options.preview_width
    wpercent = (width / float(im.size[0]))
    height = int((float(im.size[1]) * float(wpercent)))
    im = im.resize((width, height), Image.ANTIALIAS)

    im.save(output_file_path, quality=50, format='JPEG')
