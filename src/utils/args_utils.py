from src.constants import constants
from argparse import ArgumentParser


def get_cli_args() -> dict:
    """Gets the CLI args as a dictionary"""

    parser = ArgumentParser(epilog="A speedrun by Johnny Madigan ─=≡Σ(((╯°□°)╯")

    _add_game_of_life_args(parser)

    args = parser.parse_args()
    res = {
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
    return res


def _add_game_of_life_args(parser: ArgumentParser):
    """
    Purpose: to bulk-add all arguments in the context of the Game of Life application
    """

    # FYI: order when adding arguments = order they show up in help doc

    parser.add_argument(
        "-d",
        "--dimensions",
        nargs=2,
        type=int,
        default=[constants.DEFAULT_DIMENSION_X, constants.DEFAULT_DIMENSION_Y],
        metavar=("x", "y"),
        help="Dimensions for the size of the cell matrix",
    )

    parser.add_argument(
        "-r",
        "--random",
        type=int,
        default=constants.DEFAULT_RANDOM,
        metavar="%",
        help="Chance (out of 100%%) for a cell to be alive initially",
    )

    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        default=constants.DEFAULT_NUM_OF_GENERATIONS,
        metavar="count",
        help="Number of generations",
    )

    parser.add_argument(
        "-u",
        "--updates-per-second",
        type=int,
        default=constants.DEFAULT_UPDATES_PER_S,
        metavar="count",
        help="Refresh rate of generations per second",
    )

    parser.add_argument(
        "--ghost",
        type=str,
        default=constants.DEFAULT_IS_GHOST_MODE,
        metavar="'true' or 'false'",
        help="Toggle ghost mode (older generations fading away)",
    )

    parser.add_argument(
        "-w",
        "--wrap",
        type=str,
        default=constants.DEFAULT_IS_WRAP_MODE,
        metavar="'true' or 'false'",
        help="Toggle wrap mode (neighbourhoods wrap around matrix bounds)",
    )

    parser.add_argument(
        "--survival-rule",
        type=str,
        default=constants.DEFAULT_SURVIVAL_RULE,
        metavar="comma separated numbers",
        help="Number of alive neighbour cells for (alive) host cell to survive",
    )

    parser.add_argument(
        "--resurrection-rule",
        type=str,
        default=constants.DEFAULT_RESURRECTION_RULE,
        metavar="comma separated numbers",
        help="Number of alive neighbour cells for (dead) host cell to resurrect",
    )

    parser.add_argument(
        "-n",
        "--neighbourhood",
        type=str,
        default=constants.DEFAULT_NEIGHBOURHOOD.value,
        metavar="type",
        help="Type of neighbourhood: 'm' for Moore, 'v' for VonNeumann",
    )

    parser.add_argument(
        "--radius",
        type=int,
        default=constants.DEFAULT_RADIUS,
        metavar="size",
        help="Radius a.k.a size of neighbourhood",
    )

    # parser.add_argument(
    #     "--gif",
    #      #type=parse_radius_type,
    #     #default=constants.DEFAULT_RADIUS,
    #     help="Will export simulation as GIF",
    # )
