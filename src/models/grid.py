from src.constants import constants
from src.enums.cell_state import CellState


class Grid:  # rename to world
    """
    Represents the game world/grid/matrix.
    - Holds the current state of all cells in the world
    - Current state can be extracted in string format
    - Can evolve the state based on game rules
    """

    def __init__(
        self,
        width: int = constants.DEFAULT_WIDTH,
        height: int = constants.DEFAULT_HEIGHT,
        initial_cells: int | None = None,
    ):
        self._width: int = width
        self._height: int = height
        self._initial_cells = initial_cells
        self._matrix: list[list[str]] = [
            [(CellState.random().value * 2) for _ in range(width)]
            for _ in range(height)
        ]

    # @property
    def test_print_matrix_as_str(self):
        """
        Returns matrix in string format
        """

        print("\n".join(["".join(col) for col in self._matrix]))
        # test = "".join([row for row in self._matrix])
        # return self._matrix

    def set_cell(self, x, y, char):  # chain to enum type
        self._matrix[x][y] = char

    def evolve(self, num_of_cycles: int):
        for i in range(0, num_of_cycles):
            new_matrix = [
                [(CellState.random().value * 2) for _ in range(self._width)]
                for _ in range(self._height)
            ]
            str_res = "\n".join(["".join(row) for row in new_matrix])
            yield str_res

    # def evolve(self):
    #     pass

    # def as_string(self, bbox):
    #     pass

    # def __str__(self):
    #     pass
