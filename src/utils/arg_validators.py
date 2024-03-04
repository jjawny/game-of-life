from argparse import ArgumentTypeError
from src.constants import constants


def parse_dimension_type(value: str) -> int:
    """Throws if dimension value is not valid"""
    try:
        dimension = int(value)  # throws ValueError if type cast fails

        if not (constants.MIN_DIMENSION <= dimension <= constants.MAX_DIMENSION):
            raise ArgumentTypeError(
                f"Dimensions must be {constants.MIN_DIMENSION}..{constants.MAX_DIMENSION} inclusive"
            )

        return dimension
    except ValueError:
        raise ArgumentTypeError("Dimensions must be integers")


def parse_generations_type(value: str) -> int:
    """Throws if generations is not valid"""
    try:
        generations = int(value)

        if not (constants.MIN_GENERATIONS <= generations <= constants.MAX_GENERATIONS):
            raise ArgumentTypeError(
                f"Generations must be {constants.MIN_GENERATIONS}..{constants.MAX_GENERATIONS} inclusive"
            )

        return generations
    except ValueError:
        raise ArgumentTypeError("Generations must be an integer")


def parse_updates_per_second_type(value: str) -> int:
    """Throws if updates per second is not valid"""
    try:
        updates = int(value)

        if not (constants.MIN_UPDATES_PER_S <= updates <= constants.MAX_UPDATES_PER_S):
            raise ArgumentTypeError(
                f"Updates per second must be {constants.MIN_UPDATES_PER_S}..{constants.MAX_UPDATES_PER_S} inclusive"
            )

        return updates
    except ValueError:
        raise ArgumentTypeError("Updates per second must be an integer")


def parse_rule_type(values: str):
    """
    - Given numbers comma separated, returns a set of those parsed numbers
    - Throws if any number is not an integer
    - Throws if any number is not in bounds
    """
    is_in_bounds = lambda val: constants.MIN_RULE <= val <= constants.MAX_RULE

    try:
        rule_numbers = {int(val.strip()) for val in values.split(",")}
        rule_numbers_in_bounds = set(filter(is_in_bounds, rule_numbers))

        # If any num of rules were not in bounds
        if len(rule_numbers_in_bounds) < len(rule_numbers):
            raise ArgumentTypeError(
                f"Rule numbers must be {constants.MIN_RULE}..{constants.MAX_RULE} inclusive"
            )

        return rule_numbers
    except ValueError:
        raise ArgumentTypeError(f"Rule numbers must be (comma separated) integers")


def parse_random_type(value: str) -> int:
    """Throws if random value is not valid"""
    try:
        random = int(value)

        if not (constants.MIN_RANDOM <= random <= constants.MAX_RANDOM):
            raise ArgumentTypeError(
                f"Random % must be {constants.MIN_RANDOM}..{constants.MAX_RANDOM} inclusive"
            )

        return random
    except ValueError:
        raise ArgumentTypeError("Random % must be an integer")


def parse_ghost_type(value: str) -> bool:
    """Returns the parsed value"""
    return _parse_yes_or_no(value, "Ghost mode")


def parse_wrap_type(value: str) -> bool:
    """Returns the parsed value"""
    return _parse_yes_or_no(value, "Wrap mode")


def _parse_yes_or_no(value: str, arg_name: str = "Argument") -> bool:
    """Throws if value is not 'yes' or 'no'"""
    y, n, v = "yes", "no", value.lower()

    if v in (y, n):
        return v == y
    else:
        raise ArgumentTypeError(f"{arg_name} must be '{y}' or '{n}'")
