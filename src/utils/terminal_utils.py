import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_banner(offset: int = 0):
    """
    - Gets the full banner as a single string
    - Optional offset (will auto center)
    """

    offset_str = " " * max(0, offset - 11)  # 11 = current chars from start to middle

    lines = [
        r" .---.  .----. .-.",
        r"/   __}/  {}  \| |",
        r"\  {_ }\      /| `--.",
        r" `---'  `----' `----'",
        r" GAME     of    LIFE",
        r"  by Johnny Madigan",
    ]

    res = "\n".join([f"{offset_str}{line}" for line in lines])
    return res


def get_generations_footer(count: int, offset: int = 0):
    """Prints the generation count footer line w optional offset (will auto center)"""

    offset_str = " " * max(0, offset - 8)  # 8 = current chars from start to middle

    res = f"{offset_str}Generation #{count}"
    return res
