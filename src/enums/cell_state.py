from enum import Enum
import random


class CellState(Enum):
    """
    SUMMARY:
        - Cell state represented by ASCII chars
        - These chars (on most OS) are proportioned 1x2
        - To represent a true square, each state is 2x a char
    """

    ALIVE = "\u2588\u2588"      # '██'
    WELL_DONE = "\u2593\u2593"  # '▓▓'
    MEDIUM = "\u2592\u2592"     # '▒▒'
    RARE = "\u2591\u2591"       # '░░'
    DEAD = "\u0020\u0020"       # '  '

    @classmethod
    def random(cls):
        return random.choice(list(cls))
