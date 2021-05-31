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


def get_words(input_hocr):
    result = []

    with open(input_hocr, "rt") as f:
        hocr = f.read()
        doc = html.fromstring(hocr.encode())
        result = doc.xpath("//*[@class='ocrx_word']")

    return result
