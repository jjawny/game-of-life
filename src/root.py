import os
import sys
from src.models.arg_parser_wrapper import ArgParserWrapper
from src.models.grid import Grid
from src.models.settings import Settings
from typing import List
from time import sleep


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def render_all_frames(grid: Grid, settings: Settings):
    # clear()
    # construct final str with all items (a frame)s
    # print(Grid.cols, Grid.rows)
    # print(grid.test_print_matrix_as_str())
    print(settings.generations)
    generator = grid.evolve(settings.generations)

    for gen in generator:
        sleep(0.1)
        clear()
        print(gen)

    # for i in range(0, settings.generations):
    # print(i)

    # for i in range(0, grid.rows):
    #     print("\u2593" * grid.cols)


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
    generations = args.generations
    print("generations: ", generations)
    settings = Settings(generations=generations)
    print("assinging width height generations", width, height, generations)
    grid = Grid(width=width, height=height)
    render_all_frames(grid, settings)
