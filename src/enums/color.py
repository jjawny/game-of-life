from enum import Enum


class Color(Enum):
    # ANSI escape codes
    FG_ERROR = "\033[91m"
    FG_DISABLED = "\033[90m"
    BG_HIGHLIGHT = "\033[47m"
    RESET = "\033[0m"
