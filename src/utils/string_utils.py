def get_banner(line_width: int = 0):
    """Gets the banner as a single string, optionally centered"""

    lines = [
        r" .---.  .----. .-.   ",
        r"/   __}/  {}  \| |   ",
        r"\  {_ }\      /| `--.",
        r" `---'  `----' `----'",
        r" GAME     of    LIFE ",
        r"  by Johnny Madigan  ",
    ]

    res = "\n".join([line.center(line_width + 1) for line in lines])
    return res
