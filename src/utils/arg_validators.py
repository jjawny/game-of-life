from argparse import ArgumentTypeError
from src.constants import constants


def valid_dimension_type(value: str) -> int:
    """
    Throws if dimension value is not valid
    """
    try:
        dimension = int(value)  # throws ValueError if type cast fails

        if dimension < constants.MIN_DIMENSION or dimension > constants.MAX_DIMENSION:
            raise ArgumentTypeError(f"Dimensions must be within {min}..{max} inclusive")

        return dimension
    except ValueError:
        raise ArgumentTypeError("Dimensions must be integers")
