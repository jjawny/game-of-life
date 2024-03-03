from argparse import ArgumentParser

from src.constants import constants
from src.utils.arg_validators import (
    valid_wrap_type,
    valid_ghost_type,
    valid_dimension_type,
    valid_generations_type,
    valid_updates_per_second_type,
)


class ArgParserWrapper(ArgumentParser):
    def add_game_of_life_args(self):
        """
        Purpose: to bulk-add all arguments in the context of the Game of Life application
        """

        self.add_argument(
            "-d",
            "--dimensions",
            nargs=2,
            type=valid_dimension_type,
            default=[constants.DEFAULT_DIMENSION_X, constants.DEFAULT_DIMENSION_Y],
            metavar=("x", "y"),
            help="Dimensions for the size of the cell matrix",
        )

        self.add_argument(
            "-g",
            "--generations",
            type=valid_generations_type,
            default=constants.DEFAULT_NUM_OF_GENERATIONS,
            metavar="count",
            help="Num of generations",
        )

        self.add_argument(
            "-u",
            "--updates-per-second",
            type=valid_updates_per_second_type,
            default=constants.DEFAULT_UPDATES_PER_S,
            metavar="count",
            help="Refresh rate for num of generations per second",
        )

        self.add_argument(
            "--ghost",
            type=valid_ghost_type,
            default=constants.DEFAULT_IS_GHOST_MODE,
            metavar="'yes' or 'no'",
            help="Toggle ghost mode (older generations fading away)",
        )

        self.add_argument(
            "-w",
            "--wrap",
            type=valid_wrap_type,
            default=constants.DEFAULT_IS_WRAP_MODE,
            metavar="'yes' or 'no'",
            help="Toggle wrap mode (neighbourhoods wrap around matrix bounds)",
        )
