from packages.aims_geometry.geometry import polygon_area, polyline_length


def test_polyline_length():
    assert polyline_length([[0, 0, 0], [3, 4, 0]]) == 5


def test_polygon_area():
    assert polygon_area([[0, 0, 0], [10, 0, 0], [10, 10, 0], [0, 10, 0]]) == 100
