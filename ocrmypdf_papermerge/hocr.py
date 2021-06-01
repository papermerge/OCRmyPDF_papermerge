import re
from lxml import html


class BBox:

    PATTERN = r"(?P<x1>\d+)\s+(?P<y1>\d+)\s+(?P<x2>\d+)\s+(?P<y2>\d+)"

    @classmethod
    def from_string(klass, title):
        match = re.search(BBox.PATTERN, title)
        if match:
            x1 = int(match.group('x1'))
            y1 = int(match.group('y1'))
            x2 = int(match.group('x2'))
            y2 = int(match.group('y2'))

            return BBox(x1, y1, x2, y2)

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def __str__(self):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        return f"bbox {x1} {y1} {x2} {y2}"


class Word:

    def __init__(self, html_element):
        self.id = html_element.get('id')
        self.text = html_element.text
        self.title = html_element.get('title')
        self.bbox = BBox.from_string(self.title)

    @property
    def x(self):
        return self.bbox.x1

    @property
    def y(self):
        return self.bbox.y1

    @property
    def width(self):
        return self.bbox.width

    @property
    def height(self):
        return self.bbox.height

    def __str__(self):
        _id = self.id
        _text = self.text

        return f"Word(id={_id}, text={_text})"


def get_words(input_hocr):
    html_elements = []

    with open(input_hocr, "rt") as f:
        hocr = f.read()
        doc = html.fromstring(hocr.encode())
        html_elements = doc.xpath("//*[@class='ocrx_word']")

    words = [
        Word(html_el) for html_el in html_elements
    ]

    return words
