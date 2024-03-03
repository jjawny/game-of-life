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
    width: int = constants.DEFAULT_WIDTH
    height: int = constants.DEFAULT_HEIGHT
    generations: int = constants.DEFAULT_GENERATIONS
    updates_per_s: int = constants.DEFAULT_UPDATES_PER_S
    is_ghost_mode: bool = constants.DEFAULT_IS_GHOST_MODE

    # State of cells
    _curr_gen: CellMatrix = CellMatrix()
    _prev_gens: list[CellMatrix] = []  # newest -> oldest

    # Index = priority (lowest -> highest)
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
        return self._curr_gen

    def assign_new_cell_matrix(self, matrix: CellMatrix):
        self._prev_gens = []
        self._curr_gen = matrix

    def generations_generator(self):
        for _ in range(0, self.generations):
            self._get_next_generation()
            # yield self._curr_gen.as_str
            yield (
                self._combine_all_gens_as_str()
                if self.is_ghost_mode
                else self._curr_gen.as_str
            )

    def _get_next_generation(self):
        # EVOLVE: Keep a copy of the current matrix before mutating
        curr_gen_copy: CellMatrix = copy(self._curr_gen)
        self._curr_gen.mutate()

        # GHOST: Store most recent 3 generations (number based on amount of non DEAD/ALIVE cell states)
        # apply ghost affect progressively
        self._prev_gens.insert(0, curr_gen_copy)
        self._prev_gens = self._prev_gens[:3]

        for idx, state in enumerate(self._ghost_state_list):
            if 0 <= idx < len(self._prev_gens):
                gen = self._prev_gens[idx]
                gen.change_state(state)

        # TODO: the board stays a matrix until printing, during printing we add the border

        return self._curr_gen

    def _combine_all_gens_as_str(self):
        # Convert from cell states to cell priority matrices

        layers: list[list[list[int]]] = [
            np.vectorize(self._cell_to_priority)(self._curr_gen.matrix)
        ]

        for gen in self._prev_gens:
            layers.append(np.vectorize(self._cell_to_priority)(gen.matrix))

        # Flatten/reduce/combine into 1 then convert from priority back to cell states, then string
        combined_matrix: list[list[int]] = np.maximum.reduce(layers, axis=0)
        combined_matrix_cell_states: list[list[str]] = np.array(
            self._priority_state_list
        )[combined_matrix].tolist()

        as_str = "\n".join(["".join(row) for row in combined_matrix_cell_states])

        return as_str

    def _cell_to_priority(self, value: str) -> int:
        priority = (
            self._priority_state_list.index(value)
            if value in self._priority_state_list
            else -1
        )
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
