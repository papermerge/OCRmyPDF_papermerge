import unittest

from ocrmypdf_papermerge.hocr import BBox


class TestHocr(unittest.TestCase):

    def test_bbox(self):
        bbox = BBox.from_string("bbox 1024 275 1328 308; baseline 0.016 -5;")

        self.assertEqual(bbox.x1, 1024)
        self.assertEqual(bbox.y1, 275)
        self.assertEqual(bbox.x2, 1328)
        self.assertEqual(bbox.y2, 308)
        self.assertEqual(str(bbox), "bbox 1024 275 1328 308")

