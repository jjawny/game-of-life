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
        self._width: int = width
        self._height: int = height
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
                [(CellState.random().value) for _ in range(self._width)]
                for _ in range(self._height)
            ]
            str_res = "\n".join(["".join(row) for row in new_matrix])
            yield str_res

    def _get_next_generation(self):
        survival_rule = [2, 3]  # n or m live neighbours must be alive
        birth_rule = [3]  # n live neightbours must be alive

        # begin w placeholder (do not mutate original) set all cells to dead, mirrors the same size as current
        self._matrix: list[list[str]] = [
            [CellState.DEAD.value for _ in range(self._width)]
            for _ in range(self._height)
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
                neighbours = self._calc_moore_neighbours(cell_coords, radius)
            case Neighbourhoods.VON_NEUMANN:
                neighbours = self._calc_von_neighbours(cell_coords, radius)
            case _:
                pass
        # TODO: wrap
        # TODO: bounds
        return neighbours

    def _calc_moore_neighbours(
        self, cell_coords: tuple[int, int], radius: int = 1
    ) -> set[tuple[int, int]]:
        """
        Calculates the Moore neighbours surrounding a given cell

        Note: Is not responsible for neighbours out of bounds

        Algorithm summary:
            - Starting from the given radius, saves the perimiter coords (cells each side)
            - Progressively decreases the radius saving the next perimiter
            - Returns a set of cell coords
        """
        x = cell_coords[0]
        y = cell_coords[1]
        neighbours: set[tuple[int, int]] = set()
        get_perimiter_width = lambda radius: (radius * 2) + 1

        for r in range(radius, 0, -1):
            perimeter = self._get_perimeter(
                bottom_left_coords=(x - r, y - r),
                top_right_coords=(x + r, y + r),
                width=get_perimiter_width(r),
            )

            [neighbours.add(cell) for cell in perimeter.get("top", [])]
            [neighbours.add(cell) for cell in perimeter.get("right", [])]
            [neighbours.add(cell) for cell in perimeter.get("bottom", [])]
            [neighbours.add(cell) for cell in perimeter.get("left", [])]

        return neighbours

    def _calc_von_neighbours(
        self, cell_coords: tuple[int, int], radius: int = 1
    ) -> set[tuple[int, int]]:
        """
        Calculates the Von Neumann neighbours surrounding a given cell

        Note: Is not responsible for neighbours out of bounds

        Algorithm summary:
            - Starting from the given radius, saves the perimiter coords (cells each side)
            - Progressively decreases the radius saving the next perimiter
            - To achieve Von Neumann neighbourhood shape
                - Begin by trimming cells from all perimiter sides (equally from both ends leaving middle cells)
                - Decrement the amount to trim as get closer to the center cell
            - Returns a set of cell coords
        """
        x = cell_coords[0]
        y = cell_coords[1]
        neighbours: set[tuple[int, int]] = set()
        get_perimiter_width = lambda radius: (radius * 2) + 1

        for r in range(radius, 0, -1):
            perimeter = self._get_perimeter(
                bottom_left_coords=(x - r, y - r),
                top_right_coords=(x + r, y + r),
                width=get_perimiter_width(r),
            )

            top_trimmed = self._trim_both_sides(perimeter.get("top", []), r)
            right_trimmed = self._trim_both_sides(perimeter.get("right", []), r)
            bottom_trimmed = self._trim_both_sides(perimeter.get("bottom", []), r)
            left_trimmed = self._trim_both_sides(perimeter.get("left", []), r)

            [neighbours.add(cell) for cell in top_trimmed]
            [neighbours.add(cell) for cell in right_trimmed]
            [neighbours.add(cell) for cell in bottom_trimmed]
            [neighbours.add(cell) for cell in left_trimmed]

        return neighbours

    def _get_perimeter(
        self,
        bottom_left_coords: tuple[int, int],
        top_right_coords: tuple[int, int],
        width: int,
    ) -> dict:
        """
        Given 2 corner coords for a square:
            - Calcs the rest of the coords completing all sides
            - Returns a dict containing a list of coords per side
        """
        perimeter_sides = {"top": [], "right": [], "bottom": [], "left": []}

        perimeter_sides["top"] = [
            (top_right_coords[0] - x, top_right_coords[1]) for x in range(width)
        ]
        perimeter_sides["right"] = [
            (top_right_coords[0], top_right_coords[1] - y) for y in range(width)
        ]
        perimeter_sides["bottom"] = [
            (bottom_left_coords[0] + x, bottom_left_coords[1]) for x in range(width)
        ]
        perimeter_sides["left"] = [
            (bottom_left_coords[0], bottom_left_coords[1] + y) for y in range(width)
        ]

        return perimeter_sides

    def _trim_both_sides(self, list: list, val: int) -> list:
        """
        Trims start and end of a given list
        """
        if val < 0:
            return list

        try:
            return list[val : len(list) - val]
        except IndexError:
            # Swallow exception caught when over-trimming (expecting an empty list)
            return []

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
        # - index stuff
        #   - The value for how far any 'X' is from the host's X maps to h
        # - this value maps to the 'padding'
        # - padding shrinks the window (value applied to both sides to keep window centered)
        #  - as 'X' gets closer to host's X, the window increases
        # - this is how we achieve von neumann "diamond" shape
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
