from src.utils.gif_utils import _convert_to_img_bytes, _get_inches_xy
from PIL import Image
import pytest


@pytest.fixture
def mock_cell_matrix_strings() -> list[str]:
    # Pillow throws when trying to create GIF (append Images) w different sizes
    # Matplotlib renders chars varying slightly in width/height (points) even though hardcoding points per char
    # To handle this, we do not remove the padding around the plot to ensure all images have the same dimensions
    # To mock this, supply the following cell matrices w variations of cell states/placement
    return [
        """╭┈┈┈┈┈┈┈┈╮
        ┊▓▓░░▓▓░░┊
        ┊░░▓▓░░▓▓┊
        ┊▓▓░░▓▓░░┊
        ┊░░▓▓░░▓▓┊
        ╰┈┈┈┈┈┈┈┈╯""",
        """╭┈┈┈┈┈┈┈┈╮
        ┊▓▓▓▓▓▓░░┊
        ┊    ▓▓  ┊
        ┊▓▓  ▓▓  ┊
        ┊  ▓▓▓▓  ┊
        ╰┈┈┈┈┈┈┈┈╯""",
        """╭┈┈┈┈┈┈┈┈╮
        ┊░░▓▓▓▓░░┊
        ┊▓▓    ▓▓┊
        ┊▓▓    ▓▓┊
        ┊░░▓▓▓▓░░┊
        ╰┈┈┈┈┈┈┈┈╯""",
        """╭┈┈┈┈┈┈┈┈╮
        ┊▓▓    ░░┊
        ┊▓▓▓▓  ▓▓┊
        ┊▓▓  ▓▓▓▓┊
        ┊▓▓    ▓▓┊
        ╰┈┈┈┈┈┈┈┈╯""",
        """╭┈┈┈┈┈┈┈┈╮
        ┊░░▓▓  ▓▓┊
        ┊  ░░▓▓  ┊
        ┊    ▓▓░░┊
        ┊    ▓▓  ┊
        ╰┈┈┈┈┈┈┈┈╯""",
    ]


def test_convert_to_img_bytes_all_same_size_success(mock_cell_matrix_strings):
    img_bytes_list = []
    x, y = _get_inches_xy(mock_cell_matrix_strings[0])

    for s in mock_cell_matrix_strings:
        img_bytes_list.append(_convert_to_img_bytes(s, x, y))

    images = [Image.open(img) for img in img_bytes_list]
    size_to_assert = images[0].size

    assert all(img.size == size_to_assert for img in images)
