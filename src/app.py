import os
import sys
import math

from src.models.arg_parser_wrapper import ArgParserWrapper
from src.models.cell_matrix import CellMatrix
from src.models.game_state import game_state

from time import sleep


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def apply_initial_settings():
    """Applies the initial settings from CLI args"""
    # Parse
    parser = ArgParserWrapper(
        description="Custom game settings",
        epilog="A speedrun by Johnny Madigan ─=≡Σ(((╯°□°)╯",
    )
    parser.add_game_of_life_args()
    args = parser.parse_args()

    # Apply
    game_state.cols, game_state.rows = args.dimensions
    game_state.num_of_generations = args.generations
    game_state.updates_per_s = args.updates_per_second
    game_state.is_ghost_mode = args.ghost
    game_state.is_wrap_mode = args.wrap
    game_state.is_step_mode = args.step
    game_state.survival_rule = args.survival_rule
    game_state.resurrection_rule = args.resurrection_rule
    game_state.random = args.random
    game_state.neighbourhood = args.neighbourhood
    game_state.radius = args.radius


def render_main_menu():
    """Renders the main menu and reads user inputs"""
    ...


def print_banner():
    lines = [
        r"               .---.  .----. .-.   "
        r"              /   __}/  {}  \| |   "
        r"              \  {_ }\      /| `--."
        r"               `---'  `----' `----'"
        r"               GAME     of    LIFE "
        r"                by Johnny Madigan  "
    ]

    for line in lines:
        print(line)
        sleep(5)


def print_banner_static(offset: int = 0):
    '''Print banner and optionally offset (based on center)'''
    offset_centered = offset - 11 # current chars from start to middle
    offset_str = ' ' * offset_centered

    print(f"{offset_str}{r" .---.  .----. .-."}")
    print(f"{offset_str}{r"/   __}/  {}  \| |"}")
    print(f"{offset_str}{r"\  {_ }\      /| `--."}")
    print(f"{offset_str}{r" `---'  `----' `----'"}")
    print(f"{offset_str}{r" GAME     of    LIFE"}")

    # 11 -> right = center of banner, we have the center of grid available so move banner to start from center (-11 to bring back to middle)

def simulate():
    """Starts the simulation based on the settings"""

    # TODO: temporarily inject the glider for testing, need to explore regression/unit testing in python
    glider: list[tuple[int, int]] = [
        # x, y
        (0, 2),
        (1, 1),
        (2, 1),
        (2, 2),
        (2, 3),
    ]
    initial_matrix = CellMatrix(
        cols=game_state.cols,
        rows=game_state.rows,
        seed=glider,
        is_wrap=game_state.is_wrap_mode,
        survival_rule=game_state.survival_rule,
        resurrection_rule=game_state.resurrection_rule,
        random=game_state.random,
        neighbourhood=game_state.neighbourhood,
        radius=game_state.radius,
    )
    game_state.assign_new_cell_matrix(initial_matrix)

    # Actual code
    generations = game_state.generations_generator()
    delay_s = 1 / game_state.updates_per_s

    # Print initial cells
    print(game_state.curr_gen.as_str)

    for g in generations:
        sleep(delay_s)
        clear_screen()
        print(g)


def main() -> None:
    """Extracted main method to be optionally triggered by another script"""

    apply_initial_settings()
    render_main_menu()
    simulate()
