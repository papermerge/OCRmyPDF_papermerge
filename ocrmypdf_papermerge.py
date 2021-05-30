from ocrmypdf import hookimpl
from ocrmypdf.builtin_plugins.tesseract_ocr import TesseractOcrEngine
from ocrmypdf._exec import tesseract


def generate_svg(input_file, input_hocr, options):
    """
    Generates page SVG with embedded raster image and text overlay.
    """
    print(
        f"GENERATE_SVG: input_file: {input_file}, input_hocr: {input_hocr}"
    )


def generate_preview(intput_file, options):
    """
    Generates page preview as jpeg
    """
    pass


class PapermergeCustomEngine(TesseractOcrEngine):

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
        )
        generate_preview(
            input_file=input_file,
            options=options
        )
        generate_svg(
            input_file=input_file,
            input_hocr=output_hocr,
            options=options
        )


@hookimpl
def get_ocr_engine():
    return PapermergeCustomEngine()


@hookimpl
def add_options(parser):
    parser.add_argument(
        '--svg-output-folder',
        help="Folder where to write SVG generated files"
    )