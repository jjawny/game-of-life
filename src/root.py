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
    generations = grid.generations_generator(settings.generations_count)
    delay_s = 1 / settings.updates_per_s

    for g in generations:
        sleep(delay_s)
        clear()
        print(g)

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
    updates_per_second = args.updates_per_second

    print("generations: ", generations)
    settings = Settings(generations_count=generations, updates_per_s=updates_per_second)
    print("assinging width height generations", width, height, generations)
    grid = Grid(width=width, height=height)
    render_all_frames(grid, settings)
