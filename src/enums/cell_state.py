from enum import Enum
import random

class CellState(Enum):
    FULL        = "\u2588"  # '█'
    WELL_DONE   = "\u2593"  # '▓'
    MEDIUM      = "\u2592"  # '▒'
    RARE        = "\u2591"  # '░'
    BLANK       = "\u0020"  # ' '

    @classmethod
    def random(cls):
        return random.choice(list(cls))
