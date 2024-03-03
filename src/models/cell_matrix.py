from src.enums.neighbourhoods import Neighbourhoods
from src.enums.cell_state import CellState
from src.constants import constants


class CellMatrix:
    """Represents a single matrix of cells."""

    def __init__(
        self,
        width: int = constants.DEFAULT_WIDTH,
        height: int = constants.DEFAULT_HEIGHT,
        seed: list[tuple[int, int]] = [],
    ):
        self._ghost_generations: list[list[str]] = []
        self._matrix: list[list[str]] = [
            [(CellState.DEAD.value) for _ in range(width)] for _ in range(height)
        ]
        self.apply_cells(seed)

    @property
    def cols(self):
        """Get the number of cols (X-axis count aka width)"""
        return len(self._matrix[0])

    @property
    def rows(self):
        """Get the number of rows (Y-axis count aka height)"""
        return len(self._matrix)

    @property
    def matrix(self):
        """Returns the RAW matrix"""
        return self._matrix

    @property
    def as_str(self):
        """Returns the matrix in string format"""
        # Combine each row into a single string then combine all rows w newlines
        res = "\n".join(["".join(row) for row in self._matrix])
        return res

    @property
    def alive_cell_coords(self):
        """Returns the coordinates for the alive cells"""
        res: list[tuple[int, int]] = []

        # TODO: remove this cmment or place somewhere more appripriate
        # the way the matrix works is:
        # [o,o,o,o,o,o]
        # [o,o,o,o,o,o]
        # [o,o,o,o,o,o]
        # len(matrix) is the rows = 3, this is along the Y-axis
        # len(matrix[0]) is the cols = 6, this is along the X-axis
        # therefore y,x as python traverses y before x
        # general rule when
        # assign traditional x and y vlues to matrix like next_matrix[y][x]
        for y, _ in enumerate(self._matrix):
            for x, cell in enumerate(self._matrix[0]):
                if cell == CellState.ALIVE.value:
                    res.append((x, y))

        return res

    def change_state(self, new_state: CellState, old_state: CellState | None = None):
        """
        If no old state is specified, will apply the new state to all cells that are NOT dead
        """
        for row in self._matrix:
            for idx, cell in enumerate(row):
                if old_state is None and cell != CellState.DEAD.value:
                    row[idx] = new_state.value
                elif old_state is not None and cell == old_state.value:
                    row[idx] = new_state.value

    def apply_cells(
        self, cells: list[tuple[int, int]], state: CellState = CellState.ALIVE
    ):
        """Adds given cells to the matrix if in bounds"""
        for cell in cells:
            y, x = cell[0], cell[1]
            is_in_bounds = 0 <= y < self.rows and 0 <= x < self.cols

            if is_in_bounds:
                self._matrix[y][x] = state.value

    def mutate(self):
        """Mutates the current cell matrix based on game rules"""
        # Placeholder w dead cells
        next_matrix = [
            [CellState.DEAD.value for _ in range(self.cols)] for _ in range(self.rows)
        ]

        # Determine if cell is alive in the next matrix
        # turn into range index for x in range(rows) for y in range(cols)
        for x, _ in enumerate(self._matrix):
            for y, _ in enumerate(self._matrix[0]):
                if self._is_alive((x, y)):
                    next_matrix[x][y] = CellState.ALIVE.value

        # todo: the board stays a matrix until printing, during printing we add the border

        self._matrix = next_matrix

    # TODO: review the logic, especially the On^2 loops rows cols x y
    def _is_alive(self, host_cell: tuple[int, int], is_wrap: bool = True):
        """Determines if a given cell is alive based on its neighbours and rules"""

        alive_neighbours = self._get_alive_neighbours(
            host_cell=host_cell, type=Neighbourhoods.MOORE, radius=1
        )

        is_alive = False
        host_cell_state = self._matrix[host_cell[0]][host_cell[1]]
        survive_rule = {2, 3}
        resurrect_rule = {3}

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

        if is_wrap:
            neighbours = {(n[0] % self.cols, n[1] % self.rows) for n in neighbours}

        for n in neighbours:
            x, y = n[0], n[1]
            is_in_bounds = 0 <= x < self.cols and 0 <= y < self.rows

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

        # TODO: swap this around X->Y as we traverse Y before X always in code/python, we get lucky because the neighbourhood is symmetrical
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
        """Spreads range between 2 integers into a list (inclusive)"""
        res = list(range(a, b + 1)) if a <= b else list(range(a, b - 1, -1))
        return res
