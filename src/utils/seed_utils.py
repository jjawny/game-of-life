from src.constants.seeds import NONE, GLIDER
from src.enums.seed import Seed


def get_seed(name: Seed) -> list[tuple[int, int]]:
    """Returns list of (x,y) coords to plant the seed"""
    res = []

    match name:
        case Seed.NONE:
            res = NONE
        case Seed.GLIDER:
            res = GLIDER
        case _:
            pass

    return res
