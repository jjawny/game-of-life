import math

from src.models.arg_parser_wrapper import ArgParserWrapper
from src.utils.setting_utils import get_settings
from src.models.cell_matrix import CellMatrix
from src.models.menu_screen import MenuScreen
from src.models.game_state import GameState
from src.models.setting import Setting
from src.utils.terminal_utils import (
    clear_screen,
    get_banner,
    get_generations_footer,
)
from time import sleep


def get_cli_args():
    """Gets the initial CLI args"""
    parser = ArgParserWrapper(epilog="A speedrun by Johnny Madigan ─=≡Σ(((╯°□°)╯")
    parser.add_game_of_life_args()
    args = parser.parse_args()
    args_dict = {
        "cols": args.dimensions[1],
        "rows": args.dimensions[0],
        "random": args.random,
        "num_of_generations": args.generations,
        "updates_per_s": args.updates_per_second,
        "is_ghost_mode": args.ghost,
        "is_wrap_mode": args.wrap,
        "survival_rule": args.survival_rule,
        "resurrection_rule": args.resurrection_rule,
        "neighbourhood": args.neighbourhood,
        "radius": args.radius,
    }
    return args_dict


def simulate(settings: list[Setting]):
    """
    Starts the simulation based on the settings

    To keep things modular, the following has no knowledge of global 'game_state'

    Throws if unable to find or parse an opt
    """

    # TODO: temporarily inject the glider for testing, need to explore regression/unit testing in python
    glider: list[tuple[int, int]] = [
        # x, y
        (0, 2),
        (1, 1),
        (2, 1),
        (2, 2),
        (2, 3),
    ]

    # Convert to dict for easy assignment
    settings_dict = {setting.name: setting.value for setting in settings}
    initial_gen = CellMatrix(
        seed=glider,
        cols=settings_dict["cols"],
        rows=settings_dict["rows"],
        random=settings_dict["random"],
        is_wrap=settings_dict["is_wrap_mode"],
        survival_rule=settings_dict["survival_rule"],
        resurrection_rule=settings_dict["resurrection_rule"],
        neighbourhood=settings_dict["neighbourhood"],
        radius=settings_dict["radius"],
    )
    game_state = GameState(initial_gen=initial_gen)

    generations = game_state.generations_generator(
        settings_dict["num_of_generations"], settings_dict["is_ghost_mode"]
    )
    delay_s = 1 / settings_dict["updates_per_s"]

    # Print initial cells (TODO: does not include banner fix this)
    print(game_state.curr_gen.as_str)
    offset = math.floor(len(game_state.curr_gen.as_str.split("\n")[0]) / 2)

    for idx, gen in enumerate(generations):
        sleep(delay_s)
        clear_screen()
        print(get_banner(offset))
        print(gen)
        print(get_generations_footer(idx + 1, offset))


def main() -> None:
    """Extracted main method to be optionally triggered by another script"""
    try:
        initial_settings = get_settings(get_cli_args())
        menu = MenuScreen(settings=initial_settings)
        settings = menu.show()
        simulate(settings=settings)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        print("")
