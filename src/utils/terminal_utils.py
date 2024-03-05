import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner(offset: int = 0):
    """Print banner w optional offset (will auto center)"""

    offset_str = ' ' * max(0, offset - 11) # 11 = current chars from start to middle

    print(f"{offset_str}{r" .---.  .----. .-."}")
    print(f"{offset_str}{r"/   __}/  {}  \| |"}")
    print(f"{offset_str}{r"\  {_ }\      /| `--."}")
    print(f"{offset_str}{r" `---'  `----' `----'"}")
    print(f"{offset_str}{r" GAME     of    LIFE"}")
    print(f"{offset_str}{r"  by Johnny Madigan"}")


def get_banner(offset: int = 0):
    """
    - Gets the full banner as a single string 
    - Optional offset (will auto center)
    """

    offset_str = ' ' * max(0, offset - 11) # 11 = current chars from start to middle
    
    lines = [
        r" .---.  .----. .-.",
        r"/   __}/  {}  \| |",
        r"\  {_ }\      /| `--.",
        r" `---'  `----' `----'",
        r" GAME     of    LIFE",
        r"  by Johnny Madigan"
    ]

    res = "\n".join([f"{offset_str}{line}" for line in lines])
    return res

def print_generation_count_footer(count: int, offset: int = 0):

    """Prints the generation count footer line w optional offset (will auto center)"""

    offset_str = ' ' * max(0, offset - 8) # 8 = current chars from start to middle

    print(f"{offset_str}Generation #{count}")
