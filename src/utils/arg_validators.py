from argparse import ArgumentTypeError
from src.constants import constants


def valid_dimension_type(value: str) -> int:
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


def valid_generations_type(value: str) -> int:
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


def valid_updates_per_second_type(value: str) -> int:
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


def valid_ghost_bool(value: str) -> bool:
    """Returns the parsed bool"""
    return _val_to_bool(value, "Ghost mode")


def valid_wrap_bool(value: str) -> bool:
    """Returns the parsed bool"""
    return _val_to_bool(value, "Wrap mode")


def _val_to_bool(value: str, arg_name: str = "Argument") -> bool:
    """Throws if value is not 'true' or 'false'"""
    t, f, v = "true", "false", value.lower()

    if v in (t, f):
        return v == t
    else:
        raise ArgumentTypeError(f"{arg_name} must be '{t}' or '{f}'")
