from nose.tools import *

import weigh_in


def test_inverses():
    """format_description and parse_description must be inverses."""
    vals = [
        (123456, 122456),
        (123456, None),
        (123456, 123456),
        (122456, 123456),
        (12345678, 12345679)
    ]
    for current_size, prev_size in vals:
        desc = weigh_in.format_description(current_size, prev_size)
        back_size = weigh_in.parse_description(desc)
        assert back_size == current_size, (desc, back_size)
