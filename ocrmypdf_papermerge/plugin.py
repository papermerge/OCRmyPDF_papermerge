from pathlib import Path

from ocrmypdf import hookimpl
from ocrmypdf._exec import tesseract
from ocrmypdf.builtin_plugins.tesseract_ocr import TesseractOcrEngine

from .generate_preview import generate_preview
from .generate_svg import generate_svg
from .utils import copy_hocr, copy_txt


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
            input_file=Path(input_file),
            preview_width=options.preview_width,
            base_dir=options.sidecar_dir,
            uuids=options.uuids.split(',')
        )
        # svg | html with embedded raster image plus
        # mapped hocr text
        generate_svg(
            Path(input_file),
            input_hocr=output_hocr,
            options=options
        )
        # keep a copy of hocr file around
        copy_hocr(
            input_file_path=Path(output_hocr),
            output_dir=options.sidecar_dir,
            uuids=options.uuids.split(',')
        )
        # actual extracted text
        copy_txt(
            input_file_path=Path(output_text),
            output_dir=options.sidecar_dir,
            uuids=options.uuids.split(',')
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
    parser.add_argument(
        '-u',
        '--uuids',
        help="A list of uuids separated by comma. "
        " Order of UUIDs matters. First UUID corresponds to first page ID, "
        " second UUID corresponds to second page ID etc "
        "Number of UUIDs should match number of pages in the document.",
    )
