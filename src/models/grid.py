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
            [(CellState.DEAD.value) for _ in range(width)] for _ in range(height)
        ]

        # glider
        self._matrix[2][0] = CellState.ALIVE.value
        self._matrix[3][1] = CellState.ALIVE.value
        self._matrix[3][2] = CellState.ALIVE.value
        self._matrix[2][2] = CellState.ALIVE.value
        self._matrix[1][2] = CellState.ALIVE.value

        self._ghost_generations: list[list[str]] = []

    # @property
    def test_print_matrix_as_str(self):
        """
        Returns matrix in string format
        """
        res = "\n".join(["".join(row) for row in self._matrix])
        return res

    def generations_generator(self, num_of_cycles: int):
        for i in range(0, num_of_cycles):
            next_gen = self._get_next_generation()
            str_res = "\n".join(["".join(row) for row in next_gen])
            yield str_res

    def _get_next_generation(self):
        # begin w placeholder (do not mutate original) set all cells to dead, mirrors the same size as current
        next_gen: list[list[str]] = [
            [CellState.DEAD.value for _ in range(len(self._matrix[0]))]
            for _ in range(len(self._matrix))
        ]
        print("getting next gen")
        for x, row in enumerate(self._matrix):
            for y, col in enumerate(self._matrix[0]):
                if self._is_alive((x, y)):
                    next_gen[x][y] = CellState.ALIVE.value
                # the board stays a matrix until printing, during printing we add the border

        self._matrix = next_gen
        return next_gen

    def _is_alive(self, host_cell: tuple[int, int], is_wrap: bool = True):
        is_alive = False
        survive_rule = {2, 3}
        resurrect_rule = {3}
        host_cell_state = self._matrix[host_cell[0]][host_cell[1]]
        alive_neighbours = self._get_alive_neighbours(
            host_cell=host_cell, type=Neighbourhoods.MOORE, radius=1
        )

        # Apply rules
        match host_cell_state:
            case CellState.ALIVE.value:
                len(alive_neighbours)
                is_alive = True if len(alive_neighbours) in survive_rule else False
            case CellState.DEAD.value:
                is_alive = True if len(alive_neighbours) in resurrect_rule else False
            case _:
                pass

        return is_alive

    def _get_alive_neighbours(
        self,
        host_cell: tuple[int, int],
        type: Neighbourhoods,
        radius: int = 1,
        is_wrap: bool = True,
    ) -> set[tuple[int, int]]:
        """
        Determines the neighbourhood (regardless of cell state) within the bounds/context of the game:
         - Gets the neighbours based on type and radius
         - (Optionally) wraps the neighbourhood
        """
        neighbours: set[tuple[int, int]] = set()
        alive_neighbours: set[tuple[int, int]] = set()

        match type:
            case Neighbourhoods.MOORE:
                neighbours = self._get_moore_neighbourhood(host_cell, radius)
            case Neighbourhoods.VON_NEUMANN:
                neighbours = self._get_von_neumann_neighbourhood(host_cell, radius)
            case _:
                pass

        # extract length into computed property so its always accurate to check bounds
        if is_wrap:
            neighbours = {
                (n[0] % len(self._matrix[0]), n[1] % len(self._matrix))
                for n in neighbours
            }

        for n in neighbours:
            x, y = n[0], n[1]
            is_in_bounds = 0 <= x < len(self._matrix[0]) and 0 <= y < len(self._matrix)

            if is_in_bounds and self._matrix[x][y] == CellState.ALIVE.value:
                alive_neighbours.add(n)

        return alive_neighbours

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
