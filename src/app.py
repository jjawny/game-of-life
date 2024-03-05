import math

from time import sleep

from src.models.arg_parser_wrapper import ArgParserWrapper
from src.models.cell_matrix import CellMatrix
from src.models.game_state import game_state
from src.models.main_menu import MainMenu
from src.models.setting import Setting
from src.utils.terminal_utils import (
    clear_screen,
    print_banner,
    print_generation_count_footer,
)
from src.constants import constants

from src.utils.arg_validators import (
    pparse_dimension_type,
    pparse_updates_per_s_type,
    pparse_radius_type,
    pparse_generations_type,
    pparse_random_type,
    pparse_neighbourhood_type,
    pparse_bool,
)


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
    game_state.set_value("radius", args.radius)
    game_state.set_value("random", args.random)
    game_state.set_value("rows", args.dimensions[0])
    game_state.set_value("cols", args.dimensions[1])
    game_state.set_value("is_wrap_mode", args.wrap)
    game_state.set_value("is_ghost_mode", args.ghost)
    game_state.set_value("neighbourhood", args.neighbourhood)
    game_state.set_value("survival_rule", args.survival_rule)
    game_state.set_value("num_of_generations", args.generations)
    game_state.set_value("updates_per_s", args.updates_per_second)
    game_state.set_value("resurrection_rule", args.resurrection_rule)


def testing_main_menu():
    """Renders the main menu and reads user inputs"""
    opts = game_state.values

    menu_options: list[Setting] = [
        Setting(
            display_name="Dimension X",
            name="cols",
            value=opts["cols"],
            parse_value_callback=pparse_dimension_type,
            helper_text=f"Matrix height/rows {constants.MIN_DIMENSION}..{constants.MAX_DIMENSION} inclusive",
        ),
        Setting(
            display_name="Dimension Y",
            name="rows",
            value=opts["rows"],
            parse_value_callback=pparse_dimension_type,
            helper_text=f"Matrix width/cols {constants.MIN_DIMENSION}..{constants.MAX_DIMENSION} inclusive",
        ),
        Setting(
            display_name="Random %",
            name="random",
            value=opts["random"],
            parse_value_callback=pparse_random_type,
            helper_text=f"Chance for cell to start alive {constants.MIN_RANDOM}..{constants.MAX_RANDOM}% inclusive",
        ),
        Setting(
            display_name="Generations",
            name="generations",
            value=opts["num_of_generations"],
            parse_value_callback=pparse_generations_type,
            helper_text=f"Number of generations {constants.MIN_GENERATIONS}..{constants.MAX_GENERATIONS} inclusive",
        ),
        Setting(
            display_name="Updates per second",
            name="updates_per_s",
            value=opts["updates_per_s"],
            parse_value_callback=pparse_updates_per_s_type,
        ),
        Setting(
            display_name="Ghost mode",
            name="is_ghost_mode",
            value=opts["is_ghost_mode"],
            possible_values=["True", "False"],
            parse_value_callback=pparse_bool,
        ),
        Setting(
            display_name="Wrap mode",
            name="is_wrap_mode",
            value=opts["is_wrap_mode"],
            possible_values=["True", "False"],
            parse_value_callback=pparse_bool,
        ),
        Setting(
            display_name="Neighbourhood",
            name="neighbourhood",
            value=opts["neighbourhood"],
            possible_values=["Moore", "VonNeumann"],
            parse_value_callback=pparse_neighbourhood_type,
        ),
        Setting(
            display_name="Radius",
            name="radius",
            value=opts["radius"],
            parse_value_callback=pparse_radius_type,
        ),
    ]

    menu = MainMenu(final_callback=testing_final_callback, options=menu_options)
    menu.render()


def testing_final_callback(settings: list[Setting]):
    """
    Starts the simulation based on the settings

    To keep things modular, the following has no knowledge of global 'game_state'

    TODO: remove game_state from global and instead have these methods as a module? decouple from game_state

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

    initial_matrix = CellMatrix(
        seed=glider,
        cols=settings_dict["cols"],
        rows=settings_dict["rows"],
        radius=settings_dict["radius"],
        random=settings_dict["random"],
        neighbourhood=settings_dict["neighbourhood"],
        is_wrap=settings_dict["is_wrap_mode"],
        # survival_rule=settings_dict["survival_rule"],
        # resurrection_rule=settings_dict["resurrection_rule"],
    )

    game_state.assign_new_cell_matrix(initial_matrix)

    generations = game_state.generations_generator(
        settings_dict["generations"], settings_dict["is_ghost_mode"]
    )
    delay_s = 1 / settings_dict["updates_per_s"]

    # Print initial cells (TODO: does not include banner fix this)
    print(game_state.curr_gen.as_str)
    offset = math.floor(len(game_state.curr_gen.as_str.split("\n")[0]) / 2)

    for idx, gen in enumerate(generations):
        sleep(delay_s)
        clear_screen()
        print_banner(offset)
        print(gen)
        print_generation_count_footer(idx + 1, offset)


def main() -> None:
    """Extracted main method to be optionally triggered by another script"""
    try:
        apply_initial_settings()
        testing_main_menu()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        print("")
