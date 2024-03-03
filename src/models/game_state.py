import threading
import numpy as np

from src.models.cell_matrix import CellMatrix
from src.enums.cell_state import CellState
from src.constants import constants
from copy import copy


class _GameState:
    _instance = None
    _lock = threading.Lock()

    # Settings
    cols: int = constants.DEFAULT_DIMENSION_X
    rows: int = constants.DEFAULT_DIMENSION_Y
    updates_per_s: int = constants.DEFAULT_UPDATES_PER_S
    is_ghost_mode: bool = constants.DEFAULT_IS_GHOST_MODE
    num_of_generations: int = constants.DEFAULT_NUM_OF_GENERATIONS

    # State of cells
    _curr_gen: CellMatrix = CellMatrix()
    _prev_gens: list[CellMatrix] = []  # newest -> oldest

    # Index = priority (lowest -> highest / dead -> alive)
    _priority_state_list = [
        CellState.DEAD.value,
        CellState.RARE.value,
        CellState.MEDIUM.value,
        CellState.WELL_DONE.value,
        CellState.ALIVE.value,
    ]

    # State that belongs to a previous generation at the corresponding index (newest -> oldest)
    _ghost_state_list = [
        CellState.WELL_DONE,
        CellState.MEDIUM,
        CellState.RARE,
    ]

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def curr_gen(self):
        """Returns the current generation's cell matrix"""
        return self._curr_gen

    def assign_new_cell_matrix(self, matrix: CellMatrix):
        """
        Assigns a new cell matrix as the current generation and resets previous generations history
        """
        self._prev_gens = []
        self._curr_gen = matrix

    def generations_generator(self):
        """
        Returns a generator for accessing each generation as the cells evolve
        """
        for _ in range(0, self.num_of_generations):
            self._get_next_generation()
            next_gen = (
                self._combine_all_gens_as_str()
                if self.is_ghost_mode
                else self._curr_gen.as_str
            )

            yield next_gen

    def _get_next_generation(self):
        """
        Gets the next generation and responsible for updating the previous generation history
        """
        curr_gen_copy: CellMatrix = copy(self._curr_gen)
        self._curr_gen.mutate()

        # GHOST:
        #   - Insert current gen at beginning (newest -> oldest)
        #   - Slice to keep only 3 most recent generations (3 is based on amount of non DEAD/ALIVE cell states)
        #   - Apply a different ghost affect, showing generations fading away as they get older
        self._prev_gens.insert(0, curr_gen_copy)
        self._prev_gens = self._prev_gens[:3]

        for idx, state in enumerate(self._ghost_state_list):
            if 0 <= idx < len(self._prev_gens):
                gen = self._prev_gens[idx]
                gen.change_state(state)

        return self._curr_gen

    def _combine_all_gens_as_str(self) -> str:
        """
        Combines all generations into a single matrix (prioritising cell state)
        """

        # Convert cell states to cell priority per layer (matrix)
        layers: list[list[list[int]]] = [
            np.vectorize(self._cell_to_priority)(self._curr_gen.matrix)
        ]

        for gen in self._prev_gens:
            layers.append(np.vectorize(self._cell_to_priority)(gen.matrix))

        # Flatten/reduce/combine layers into 1
        combined_matrix: list[list[int]] = np.maximum.reduce(layers, axis=0)

        # Convert priorities back to corresponding cell states
        combined_matrix_cell_states: list[list[str]] = np.array(
            self._priority_state_list
        )[combined_matrix].tolist()

        as_str = "\n".join(["".join(row) for row in combined_matrix_cell_states])

        return as_str

    def _cell_to_priority(self, value: str) -> int:
        """
        Maps a cell state to its priority over other cell states

        Priority = (highest -> lowest / cell states dead -> alive)
        """
        priority = -1  # assume not in list

        if value in self._priority_state_list:
            priority = self._priority_state_list.index(value)

        return priority


# Python modules are singletons by nature ∴ we can import the following.
# Singletons are often argued to be an anti-pattern and globals suck but
#   due to the simplicity of this class and what it represents, we allow
#   thread safe access to read/write settings, instead of passing a settings
#   object all over the place (unneccessary)

# For improvements, take a look at:
#   - Llama-Index's "service_context"
#   - How a logger is setup

game_state = _GameState()
