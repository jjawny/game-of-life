from src.constants.seeds import NONE, GLIDER
from src.enums.seed import Seed


def get_seed(name: Seed) -> list[tuple[int, int]]:
    """Returns a list of (x,y) coords to plant the seed"""
    match name:
        case Seed.NONE:
            return NONE
        case Seed.GLIDER:
            return GLIDER
        case _:
            return []
