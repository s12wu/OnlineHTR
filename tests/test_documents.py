from pathlib import Path
import logging

import numpy as np
import pytest

from src.utils import documents


@pytest.mark.martin
def test_Stroke_class():

    # Create test data
    test_x = np.array([1.23, 2.34, 3.45])
    test_y = np.array([4, 5, 6])
    test_meta_data = {
        'foo': 'bar',
        42: 1337,
    }

    # Test construction of stroke
    stroke = documents.Stroke(
        test_x,
        test_y,
        test_meta_data
    )

    # Test storage
    np.testing.assert_array_equal(stroke.x, test_x)
    np.testing.assert_array_equal(stroke.y, test_y)
    np.testing.assert_array_equal(stroke.meta_data.keys(),
                                  test_meta_data.keys())
    for key in stroke.meta_data:
        assert stroke.meta_data[key] == test_meta_data[key]

@pytest.mark.martin
def test_XournalDocument():

    x_document = documents.XournalDocument(path=Path.home() / Path('data/code/carbune2020_implementation/data/datasets/2024-01-20-xournal_dataset.xoj'))

    assert len(x_document.pages) == 2

    assert len( x_document.pages[0].layers[0].strokes ) == 0

    assert x_document.pages[1].layers[0].texts[0].text == 'sample_name: hello_world'
    assert x_document.pages[1].layers[0].texts[1].text == 'label: Hello World!'
    # TODO: Add some check about length of strokes

    # TODO: Check all other parameters like background and pagea attributes; check load_data of XournalDocument for that. Also DPI.
    # TODO: Maybe check save_page_as_image?
    # TODO: Check path.

    # TODO: note that I won't test the dataclasses in excess to what I have done so already for Stroke class above.

    # TODO: Next: Implement and test XournalPagewiseDataset.
    # TODO: Next: Build model and test on XournalPagewiseDataset!
