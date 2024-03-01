from argparse import ArgumentTypeError
from src.constants import constants


def valid_dimension_type(value: str) -> int:
    """
    Throws if dimension value is not valid
    """
    try:
        dimension = int(value)  # throws ValueError if type cast fails

        if dimension < constants.MIN_DIMENSION or dimension > constants.MAX_DIMENSION:
            raise ArgumentTypeError(
                f"Dimensions must be within {constants.MIN_DIMENSION}..{constants.MAX_DIMENSION} inclusive"
            )

        return dimension
    except ValueError:
        raise ArgumentTypeError("Dimensions must be integers")


def valid_generations_type(value: str) -> int:
    """
    Throws if generations is not valid
    """
    try:
        generations = int(value)

        if generations < constants.MIN_GENERATIONS:
            raise ArgumentTypeError(
                f"Generations must be greater than {constants.MIN_GENERATIONS}"
            )

        return generations
    except ValueError:
        raise ArgumentTypeError("Generations must be integers")
