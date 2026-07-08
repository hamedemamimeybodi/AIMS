from packages.aims_core.adf import ADFCategory
from packages.aims_core.classification import classify_layer


def test_classify_wall_layer():
    assert classify_layer("A-WALL") == ADFCategory.WALL


def test_classify_unknown_layer():
    assert classify_layer("RANDOM-LAYER") == ADFCategory.UNKNOWN
