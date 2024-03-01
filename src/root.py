import sys
from .models.arg_parser_wrapper import ArgParserWrapper


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

    print(f"width: {width}")
    print(f"height: {height}")

    print("hello")
