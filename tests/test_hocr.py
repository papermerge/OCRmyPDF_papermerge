from ocrmypdf_papermerge.hocr import BBox


def test_bbox():
    bbox = BBox.from_string("bbox 1024 275 1328 308; baseline 0.016 -5;")

    assert bbox.x1 == 1024
    assert bbox.y1 == 275
    assert bbox.x2 == 1328
    assert bbox.y2 == 308
    assert str(bbox) == "bbox 1024 275 1328 308"
