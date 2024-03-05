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
