from src.constants import constants
import matplotlib.pyplot as plot
from datetime import datetime
from io import BytesIO
from PIL import Image
import os

DIRECTORY_NAME = "gifs"


def export_as_gif(strings: list[str], updates_per_s: int = 1):
    """
    Assumes all frames are the same size
    """
    _ensure_gif_dir_exists()

    img_bytes_list = []
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"GAMEofLIFE-{now}.gif"
    duration = (100 / updates_per_s) * len(strings)

    for s in strings:
        img_bytes_list.append(_convert_to_frame_bytes(s))

    frames = [Image.open(img) for img in img_bytes_list]
    frames[0].save(
        f"{DIRECTORY_NAME}/{file_name}",
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
    )


def _ensure_gif_dir_exists():
    if not os.path.exists(DIRECTORY_NAME):
        os.makedirs(DIRECTORY_NAME)


def _convert_to_frame_bytes(string: str):
    img_bytes = BytesIO()

    # 1. We will set fixed image dimensions with the max dimensions allowed
    #    This guarentees generated cell matrices will fit inside
    #
    #    Matplotlib (x,y) axis points do not line up with monospace chars unfortunately...
    #    Determine the "divider" values to fit a number of chars within image bounds
    #    NOTE: This requires testing to calc new dividers when max constants change
    CHAR_TO_IMG_WIDTH_DIVIDER = 4.5
    CHAR_TO_IMG_HEIGHT_DIVIDER = 4.2

    img_full_width = constants.MAX_DIMENSION / CHAR_TO_IMG_WIDTH_DIVIDER
    img_full_height = constants.MAX_DIMENSION / CHAR_TO_IMG_HEIGHT_DIVIDER

    # 2. We will get the width/height of the matrix
    #    We will apply the divider to keep these within bounds
    #    NOTE: To represent a true square, each cell consists of 2 chars, this means we need to divide width in half
    lines = string.split("\n")
    string_width = (len(lines[0]) / 2) / CHAR_TO_IMG_WIDTH_DIVIDER
    string_height = len(lines) / CHAR_TO_IMG_HEIGHT_DIVIDER

    # 3. We convert the width/height of the strings into their percentage of image's width/height
    string_width_percentage = string_width / img_full_width
    string_height_percentage = string_height / img_full_height

    # 4. To center, we want to move the graph left/down by half of its width/height
    offset_x = 0.5 - (string_width_percentage / 2)
    offset_y = 0.5 - (string_height_percentage / 2)

    # 5. Create the image
    plot.figure(figsize=(img_full_width, img_full_height))
    plot.axis("off")  # toggle "on" (comment out) for debugging
    plot.text(offset_x, offset_y, string, fontfamily="monospace")
    plot.savefig(img_bytes, format="png", dpi=100)
    plot.close()

    return img_bytes
