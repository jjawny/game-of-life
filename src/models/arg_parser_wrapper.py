from src.constants import constants
from argparse import ArgumentParser


class ArgParserWrapper(ArgumentParser):
    def add_game_of_life_args(self):
        """
        Purpose: to bulk-add all arguments in the context of the Game of Life application
        """

        # FYI: order adding arguments = order they show up in help doc

        self.add_argument(
            "-d",
            "--dimensions",
            nargs=2,
            type=int,
            default=[constants.DEFAULT_DIMENSION_X, constants.DEFAULT_DIMENSION_Y],
            metavar=("x", "y"),
            help="Dimensions for the size of the cell matrix",
        )

        self.add_argument(
            "-r",
            "--random",
            type=int,
            default=constants.DEFAULT_RANDOM,
            metavar="%",
            help="Chance (out of 100%%) for a cell to be alive initially",
        )

        self.add_argument(
            "-g",
            "--generations",
            type=int,
            default=constants.DEFAULT_NUM_OF_GENERATIONS,
            metavar="count",
            help="Number of generations",
        )

        self.add_argument(
            "-u",
            "--updates-per-second",
            type=int,
            default=constants.DEFAULT_UPDATES_PER_S,
            metavar="count",
            help="Refresh rate of generations per second",
        )

        self.add_argument(
            "--ghost",
            type=str,
            default=constants.DEFAULT_IS_GHOST_MODE,
            metavar="'true' or 'false'",
            help="Toggle ghost mode (older generations fading away)",
        )

        self.add_argument(
            "-w",
            "--wrap",
            type=str,
            default=constants.DEFAULT_IS_WRAP_MODE,
            metavar="'true' or 'false'",
            help="Toggle wrap mode (neighbourhoods wrap around matrix bounds)",
        )

        self.add_argument(
            "--survival-rule",
            type=str,
            default=constants.DEFAULT_SURVIVAL_RULE,
            metavar="comma separated numbers",
            help="Number of alive neighbour cells for (alive) host cell to survive",
        )

        self.add_argument(
            "--resurrection-rule",
            type=str,
            default=constants.DEFAULT_RESURRECTION_RULE,
            metavar="comma separated numbers",
            help="Number of alive neighbour cells for (dead) host cell to resurrect",
        )

        self.add_argument(
            "-n",
            "--neighbourhood",
            type=str,
            default=constants.DEFAULT_NEIGHBOURHOOD.value,
            metavar="type",
            help="Type of neighbourhood: 'm' for Moore, 'v' for VonNeumann",
        )

        self.add_argument(
            "--radius",
            type=int,
            default=constants.DEFAULT_RADIUS,
            metavar="size",
            help="Radius a.k.a size of neighbourhood",
        )

        # self.add_argument(
        #     "--gif",
        #      #type=parse_radius_type,
        #     #default=constants.DEFAULT_RADIUS,
        #     help="Will export simulation as GIF",
        # )
