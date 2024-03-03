import os
import sys

from src.models.arg_parser_wrapper import ArgParserWrapper
from src.models.cell_matrix import CellMatrix
from src.models.game_state import game_state

from typing import List
from time import sleep


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def apply_initial_settings():
    """Applies the initial settings from CLI args"""
    # Parse
    parser = ArgParserWrapper(
        description="Settings",
        epilog="A speedrun by Johnny Madigan ─=≡Σ(((╯°□°)╯",
    )
    parser.add_game_of_life_args()
    args = parser.parse_args()

    # Apply
    game_state.width, game_state.height = args.dimensions
    game_state.generations = args.generations
    game_state.updates_per_s = args.updates_per_second


def render_main_menu():
    """Renders the main menu and reads user inputs"""
    ...


def simulate():
    """Starts the simulation based on the settings"""
    glider: list[tuple[int, int]] = [
        (2, 0),
        (3, 1),
        (3, 2),
        (2, 2),
        (1, 2),
    ]
    initial_matrix = CellMatrix(
        width=game_state.width, height=game_state.height, seed=glider
    )
    game_state.assign_new_cell_matrix(initial_matrix)

    generations = game_state.generations_generator()
    delay_s = 1 / game_state.updates_per_s

    # Print initial
    print(game_state.curr_gen.as_str)
    # sleep(100000)

    for g in generations:
        sleep(delay_s)
        clear_screen()
        print(g)


def main() -> None:
    """Extracted main method to be optionally triggered by another script"""

    apply_initial_settings()
    render_main_menu()
    simulate()
