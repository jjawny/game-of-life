import os
import sys
from src.models.arg_parser_wrapper import ArgParserWrapper
from src.models.grid import Grid


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def render(grid: Grid):
    clear()

    for i in range(0, grid.rows):
        print("\u2593" * grid.cols)


def main() -> None:
    """
    Extracted main method to be optionally triggered by another script
    """

    parser = ArgParserWrapper(
        description="Settings",
        epilog="A speedrun by Johnny Madigan ─=≡Σ(((╯°□°)╯",
    )
    parser.add_game_of_life_args()
    args = parser.parse_args()

    width, height = args.dimensions

    print(f"width: {width}")
    print(f"height: {height}")

    grid = Grid(width=width, height=height)
    render(grid)
