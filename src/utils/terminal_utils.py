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

def print_generation_count_footer(count: int, offset: int = 0):

    """Prints the generation count footer line w optional offset (will auto center)"""

    offset_str = ' ' * max(0, offset - 8) # 8 = current chars from start to middle

    print(f"{offset_str}Generation #{count}")

def print_exit_footer(offset: int = 0):
    """Prints the exit footer"""
    offset_str = ' ' * max(0, offset - 8) # 8 = current chars from start to middle
    print(f"{offset_str}Ctrl+C to exit")
