from ocrmypdf import hookimpl
from ocrmypdf.builtin_plugins.tesseract_ocr import TesseractOcrEngine
from ocrmypdf._exec import tesseract

from .generate_preview import generate_preview
from .generate_svg import generate_svg
from .utils import (
    copy_hocr,
    copy_txt
)


class CustomEngine(TesseractOcrEngine):

    @staticmethod
    def generate_hocr(input_file, output_hocr, output_text, options):
        tesseract.generate_hocr(
            input_file=input_file,
            output_hocr=output_hocr,
            output_text=output_text,
            languages=options.languages,
            engine_mode=options.tesseract_oem,
            tessconfig=options.tesseract_config,
            timeout=options.tesseract_timeout,
            pagesegmode=options.tesseract_pagesegmode,
            user_words=options.user_words,
            user_patterns=options.user_patterns,
            thresholding=options.tesseract_thresholding
        )
        # jpeg thumbnail preview image
        generate_preview(
            input_file=str(input_file),
            options=options
        )
        # svg | html with embedded raster image plus
        # mapped hocr text
        generate_svg(
            input_file=str(input_file),
            input_hocr=output_hocr,
            options=options
        )
        # keep a copy of hocr file around
        copy_hocr(
            input_file_path=str(output_hocr),
            output_dir=options.sidecar_dir
        )
        # actual extracted text
        copy_txt(
            input_file_path=str(output_text),
            output_dir=options.sidecar_dir
        )


@hookimpl
def get_ocr_engine():
    return CustomEngine()


@hookimpl
def add_options(parser):
    parser.add_argument(
        '--sidecar-dir',
        help="Folder where to write generated files"
    )
    parser.add_argument(
        '--sidecar-format',
        help="Format of generated output",
        choices=["html", "svg"],
        default="svg"
    )
    parser.add_argument(
        '--preview-width',
        help="Base width of preview image",
        type=int,
        default=400
    )
