from argparse import ArgumentParser

from src.utils.arg_validators import valid_dimension_type
from src.constants import constants


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
            default=[constants.DEFAULT_WIDTH, constants.DEFAULT_HEIGHT],
            metavar=("width", "height"),
            help="Dimensions for the size of the grid (world)",
        )
