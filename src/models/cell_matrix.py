from src.enums.neighbourhood import Neighbourhood
from src.enums.cell_state import CellState
from src.constants import constants
import random


class CellMatrix:
    """
    Represents a single matrix of cells:
        - TODO: write about the params, same about game-state
    """

    # Dev notes:
    #   - When designing algos, remember code matrices are traversed rows first (Y-axis) before cols (X-axis)
    #   - For example "my_matrix":
    #
    #           [o,o,o,o]
    #     3(y)  [o,o,o,o]
    #           [o,o,o,o]
    #
    #              4(x)
    #
    #   - Iterating "for y in my_matrix" accesses each row ([o,o,o,o])
    #   - Iterating "for x in my_matrix[i]" accesses each col value in row (o)
    #
    #   - Store coords the traditional way you'd expect (x,y)
    #   - When applying coords to a matrix, access w "my_matrix[y][x]"

    _ghost_generations: list[list[str]] = []

    def __init__(
        self,
        seed: list[tuple[int, int]] = [],
        radius: int = constants.DEFAULT_RADIUS,
        random: int = constants.DEFAULT_RANDOM,
        cols: int = constants.DEFAULT_DIMENSION_X,
        rows: int = constants.DEFAULT_DIMENSION_Y,
        is_wrap: bool = constants.DEFAULT_IS_WRAP_MODE,
        survival_rule: set = constants.DEFAULT_SURVIVAL_RULE,
        resurrection_rule: set = constants.DEFAULT_RESURRECTION_RULE,
        neighbourhood: Neighbourhood = constants.DEFAULT_NEIGHBOURHOOD,
    ):
        # TODO: use existing custom validation functions here as well ?
        self._random = random
        self._is_wrap = is_wrap
        self._survive_rule = survival_rule
        self._resurrect_rule = resurrection_rule
        self._neighbourhood = neighbourhood
        self._radius = radius
        self._matrix: list[list[str]] = [
            [(CellState.DEAD.value) for _ in range(cols)] for _ in range(rows)
        ]
        self.apply_cells(seed) if seed else self.apply_random_cells()

    @property
    def rows(self):
        """Get the number of rows (Y-axis count aka height)"""
        return len(self._matrix)

    @property
    def cols(self):
        """Get the number of cols (X-axis count aka width)"""
        return len(self._matrix[0])

    @property
    def matrix(self):
        """Returns the RAW matrix"""
        return self._matrix

    @property
    def as_str(self):
        """Returns the matrix in string format"""
        # 1. Combine each row's values into a single string
        # 2. Combine all row strings w newlines
        res = "\n".join(["".join(row) for row in self._matrix])
        return res

    @property
    def alive_cell_coords(self):
        """Returns the coordinates for the alive cells"""
        res: list[tuple[int, int]] = []

        for y, row in enumerate(self._matrix):
            for x, cell in enumerate(row):
                if cell == CellState.ALIVE.value:
                    res.append((x, y))

        return res

    def change_state(self, new_state: CellState, old_state: CellState | None = None):
        """
        If no old state is specified, the new state will be applied to all cells that are NOT dead
        """

        is_old_state_specified = old_state is not None

        for row in self._matrix:
            for x, cell in enumerate(row):
                if not is_old_state_specified and cell != CellState.DEAD.value:
                    row[x] = new_state.value

                elif is_old_state_specified and cell == old_state.value:
                    row[x] = new_state.value

    def apply_cells(
        self, cells: list[tuple[int, int]], state: CellState = CellState.ALIVE
    ):
        """Adds given cells to the matrix if in bounds"""

        for cell in cells:
            x, y = cell[0], cell[1]
            is_in_bounds = 0 <= y < self.rows and 0 <= x < self.cols

            if is_in_bounds:
                self._matrix[y][x] = state.value

    def apply_random_cells(self, state: CellState = CellState.ALIVE):
        """Randomly creates cells with a given state"""
        for row in self._matrix:
            for x, _ in enumerate(row):
                random_percent = random.randint(0, 100)  # %
                if random_percent <= self._random:
                    row[x] = state.value

    def mutate(self):
        """Mutates the current cell matrix"""

        next_matrix = [
            [CellState.DEAD.value for _ in range(self.cols)] for _ in range(self.rows)
        ]

        # Determine if cell is alive (survive/resurrect) in the next matrix
        for y, row in enumerate(self._matrix):
            for x, _ in enumerate(row):
                if self._is_alive((x, y)):
                    next_matrix[y][x] = CellState.ALIVE.value

        self._matrix = next_matrix

    def _is_alive(self, host_cell: tuple[int, int]):
        """Determines if a given cell is alive based on its neighbours and rules"""

        is_alive = False
        host_x, host_y = host_cell[0], host_cell[1]
        host_cell_state = self._matrix[host_y][host_x]
        num_of_alive_neighbours = len(self._get_alive_neighbours(host_cell=host_cell))

        match host_cell_state:
            case CellState.ALIVE.value:
                is_alive = (
                    True if num_of_alive_neighbours in self._survive_rule else False
                )
            case CellState.DEAD.value:
                is_alive = (
                    True if num_of_alive_neighbours in self._resurrect_rule else False
                )
            case _:
                pass

        return is_alive

    def _get_alive_neighbours(self, host_cell: tuple[int, int]) -> set[tuple[int, int]]:
        """
        Determines the neighbourhood (regardless of cell state) within the bounds/context of the game:
         - Gets the neighbours based on type and radius
         - (Optionally) wraps the neighbourhood
        """
        all_neighbours: set[tuple[int, int]] = set()
        alive_neighbours: set[tuple[int, int]] = set()

        match self._neighbourhood:
            case Neighbourhood.MOORE:
                all_neighbours = self._get_moore_neighbourhood(host_cell)
            case Neighbourhood.VON_NEUMANN:
                all_neighbours = self._get_von_neumann_neighbourhood(host_cell)
            case _:
                pass

        if self._is_wrap:
            all_neighbours = {
                (n[0] % self.cols, n[1] % self.rows) for n in all_neighbours
            }

        for neighbour in all_neighbours:
            x, y = neighbour[0], neighbour[1]
            is_in_bounds = 0 <= x < self.cols and 0 <= y < self.rows

            if is_in_bounds and self._matrix[y][x] == CellState.ALIVE.value:
                alive_neighbours.add(neighbour)

        return alive_neighbours

    def _get_von_neumann_neighbourhood(
        self, host_cell: tuple[int, int]
    ) -> set[tuple[int, int]]:
        """
        Calculates the Von Neumann neighbours surrounding a given host cell
        - Travels from top to bottom (along Y-axis)
        - Each iteration saves the cells left to right (along X-axis)
        - Each iteration calcs the window along the X-axis to achieve Von Neumann
        - Is not responsible for excluding neighbours out of bounds
        - Does not save the host cell
        """
        host_x, host_y = host_cell

        lower_x = host_x - self._radius
        upper_x = host_x + self._radius
        lower_y = host_y - self._radius
        upper_y = host_y + self._radius

        # ALGO SUMMARY TO ACHIEVE VON NEUMANN:
        #   - Get lists holding all 'Y' coords:
        #       - Incrementing from host cell to radius limit [y..upper_y]
        #       - Decrementing from host cell to radius limit [y..lower_y]
        #   - The index of a given 'Y' in these lists shows how far away 'Y' is from the host
        #   - This value also maps nicely to how much padding is needed (both sides) to shrink the X-axis range (creating a window)
        #   - The further away 'Y' is = the greater the padding = the smaller the window = the Von Neumann "diamond" shape
        y_coords_up = self._spread_integers(host_y, upper_y)
        y_coords_down = self._spread_integers(host_y, lower_y)

        get_window_padding = lambda coord_range, target: (
            coord_range.index(target) if target in coord_range else -1
        )

        neighbours: set[tuple[int, int]] = set()

        for y in range(lower_y, upper_y + 1):
            padding_x = 0

            if y > host_y:
                padding_x = get_window_padding(y_coords_up, y)
            else:
                padding_x = get_window_padding(y_coords_down, y)

            # Signifies window completely closed ∴ no cells to save
            if padding_x <= -1:
                continue

            # Define X-axis window bounds
            window_lower_x = lower_x + padding_x
            window_upper_x = upper_x - padding_x

            for x in range(window_lower_x, window_upper_x + 1):
                if (x, y) != host_cell:
                    neighbours.add((x, y))

        return neighbours

    def _get_moore_neighbourhood(
        self, host_cell: tuple[int, int]
    ) -> set[tuple[int, int]]:
        """
        Calculates the Moore neighbours surrounding a given host cell
        - Travels from top to bottom (along Y-axis)
        - Each iteration saves the cells left to right (along X-axis)
        - Is not responsible for excluding neighbours out of bounds
        - Does not save the host cell
        """
        hostX, hostY = host_cell

        lowerX = hostX - self._radius
        upperX = hostX + self._radius
        lowerY = hostY - self._radius
        upperY = hostY + self._radius

        neighbours: set[tuple[int, int]] = set()

        for y in range(lowerY, upperY + 1):
            for x in range(lowerX, upperX + 1):
                if (x, y) != host_cell:
                    neighbours.add((x, y))

        return neighbours

    def _spread_integers(self, a: int, b: int) -> list[int]:
        """Spreads the range of ints between a and b (inclusive)"""
        res = list(range(a, b + 1)) if a <= b else list(range(a, b - 1, -1))
        return res
