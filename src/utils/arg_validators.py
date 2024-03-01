from argparse import ArgumentTypeError


def valid_dimension_type(value: str) -> int:
    """
    Throws if dimension value is not valid
    """
    try:
        min = 1
        max = 256
        dimension = int(value)  # throws ValueError if type cast fails

        if dimension < min or dimension > max:
            raise ArgumentTypeError(f"Dimensions must be within {min}..{max} inclusive")

        return dimension
    except ValueError:
        raise ArgumentTypeError("Dimensions must be integers")
