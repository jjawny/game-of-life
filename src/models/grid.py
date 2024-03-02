from src.constants import constants
from src.enums.cell_state import CellState
from src.enums.neighbourhoods import Neighbourhoods


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
        self._cols: int = width
        self._rows: int = height
        self._initial_cells = initial_cells
        self._matrix: list[list[str]] = [  # TODO: revert back to blank
            [(CellState.random().value) for _ in range(width)] for _ in range(height)
        ]
        self._ghost_generations: list[list[str]] = []

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

    def generations_generator(self, num_of_cycles: int):
        for i in range(0, num_of_cycles):
            new_matrix = [
                [(CellState.random().value) for _ in range(self._cols)]
                for _ in range(self._rows)
            ]
            str_res = "\n".join(["".join(row) for row in new_matrix])
            yield str_res

    def _get_next_generation(self):
        survival_rule = [2, 3]  # n or m live neighbours must be alive
        birth_rule = [3]  # n live neightbours must be alive

        # begin w placeholder (do not mutate original) set all cells to dead, mirrors the same size as current
        self._matrix: list[list[str]] = [
            [CellState.DEAD.value for _ in range(self._cols)] for _ in range(self._rows)
        ]

        # die otherwise
        # we check all cells and apply rule

        for x, row in enumerate(self._matrix):
            for y, col in enumerate(self._matrix):
                # _is_alive()
                # the board stays a matrix until printing, during printing we add the border
                ...

    def _is_alive(self, is_wrap: bool = True):
        neighbours = self._get_neighbourhood(
            cell_coords=(1, 2), type=Neighbourhoods.MOORE, radius=3
        )
        # check live_neighbours count in current state (scoped to neighbourhood), separate method here returning coords for live neighbours
        #  apply rules to determine is_alive bool
        # return bool
        is_alive = True

        return is_alive

    def _get_neighbourhood(
        self,
        cell_coords: tuple[int, int],
        type: Neighbourhoods,
        radius: int = 1,
        is_wrap: bool = True,
    ) -> set[tuple[int, int]]:
        """
        Determines the neighbourhood (regardless of cell state) within the bounds/context of the game:
         - Gets the neighbours based on type and radius
         - (Optionally) wraps the neighbourhood
         - Trims all cells out-of-bounds
        """
        neighbours: set[tuple[int, int]] = set()

        match type:
            case Neighbourhoods.MOORE:
                neighbours = self._get_moore_neighbourhood(cell_coords, radius)
            case Neighbourhoods.VON_NEUMANN:
                neighbours = self._get_von_neumann_neighbourhood(cell_coords, radius)
            case _:
                pass

        if is_wrap:
            neighbours = {(n[0] % self._cols, n[1] % self._rows) for n in neighbours}

        # TODO: bounds
        return neighbours

    def _get_von_neumann_neighbourhood(
        self, host_cell: tuple[int, int], radius: int = 1
    ) -> set[tuple[int, int]]:
        """
        Calculates the Von Neumann neighbours surrounding a given host cell
        - Travels from left to right (along X-axis)
        - Each iteration saves the cells bottom to top (along Y-axis)
        - Each iteration calcs the window along the Y-axis to achieve Von Neumann
        - Is not responsible for neighbours out of bounds
        - Does not save the host cell
        """
        if radius < 0:
            raise ValueError("Radius must be >= 0")

        host_x, host_y = host_cell

        lower_x = host_x - radius
        upper_x = host_x + radius
        lower_y = host_y - radius
        upper_y = host_y + radius

        # Algo summary:
        #   - Lists holding all 'X' coords from host left and right within radius: [x..upper_x] [x..lower_x]
        #   - The index of a given 'X' shows how far away 'X' is from the host
        #   - This value also maps nicely to how much padding is needed to shrink the Y-axis bounds (creating a window)
        #   - The further away 'X' is = the greater the padding = the smaller the window = the Von Neumann "diamond" shape
        x_coords_right = self._spread_integers(host_x, upper_x)
        x_coords_left = self._spread_integers(host_x, lower_x)

        get_window_padding = lambda x_coords, target_x: (
            x_coords.index(target_x) if target_x in x_coords else -1
        )

        neighbours: set[tuple[int, int]] = set()

        for x in range(lower_x, upper_x + 1):
            padding = (
                get_window_padding(x_coords_right, x)
                if x > host_x
                else get_window_padding(x_coords_left, x)
            )

            # Signifies no window ∴ no cells to save
            if padding <= -1:
                continue

            window_lower_y = lower_y + padding
            window_upper_y = upper_y - padding

            for y in range(window_lower_y, window_upper_y + 1):
                if (x, y) != host_cell:
                    neighbours.add((x, y))

        return neighbours

    def _get_moore_neighbourhood(
        self, host_cell: tuple[int, int], radius: int = 1
    ) -> set[tuple[int, int]]:
        """
        Calculates the Moore neighbours surrounding a given host cell
        - Travels from left to right (along X-axis)
        - Each iteration saves the cells bottom to top (along Y-axis)
        - Is not responsible for neighbours out of bounds
        - Does not save the host cell
        """
        if radius < 0:
            raise ValueError("Radius must be >= 0")

        hostX, hostY = host_cell

        lowerX = hostX - radius
        upperX = hostX + radius
        lowerY = hostY - radius
        upperY = hostY + radius

        neighbours: set[tuple[int, int]] = set()

        for x in range(lowerX, upperX + 1):
            for y in range(lowerY, upperY + 1):
                if (x, y) != host_cell:
                    neighbours.add((x, y))

        return neighbours

    def _spread_integers(self, a: int, b: int) -> list[int]:
        """
        Spreads range between 2 integers into a list (inclusive)
        """
        return list(range(a, b + 1)) if a <= b else list(range(a, b - 1, -1))
