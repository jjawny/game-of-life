import threading
import numpy as np

from src.utils.simulation_utils import cell_to_priority
from src.enums.neighbourhood import Neighbourhood
from src.models.cell_matrix import CellMatrix
from src.enums.cell_state import CellState
from src.constants import constants
from copy import copy



class _GameState:
    _instance = None
    _lock = threading.Lock()

    # Settings
    # Note: internal methods access settings dict with bracket notation, we assume the key/value pair is defined and with correct type
    _settings = {
        "radius":               constants.DEFAULT_RADIUS,
        "random":               constants.DEFAULT_RANDOM,
        "cols":                 constants.DEFAULT_DIMENSION_X,
        "rows":                 constants.DEFAULT_DIMENSION_Y,
        "is_wrap_mode":         constants.DEFAULT_IS_WRAP_MODE,
        "is_ghost_mode":        constants.DEFAULT_IS_GHOST_MODE,
        "updates_per_s":        constants.DEFAULT_UPDATES_PER_S,
        "neighbourhood":        constants.DEFAULT_NEIGHBOURHOOD,
        "survival_rule":        constants.DEFAULT_SURVIVAL_RULE,
        "resurrection_rule":    constants.DEFAULT_RESURRECTION_RULE,
        "num_of_generations":   constants.DEFAULT_NUM_OF_GENERATIONS,
    }
    

    # Generations (cell states)
    _curr_gen: CellMatrix = CellMatrix()
    _prev_gens: list[CellMatrix] = []  # newest -> oldest
    _priority_order = [
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

    # Setting-related methods
    @property
    def values(self):
        """Returns a read-only copy of the settings"""
        return self._settings.copy()

    def get_value(self, key):
        """Returns the value for a key (None if not found)"""
        return self._settings.get(key, None)

    def set_value(self, key, new_value):
        """Sets the value for a key (throws if not found)"""
        if key in self._settings:
            self._settings[key] = new_value
        else:
            raise KeyError(f"Key '{key}' not found in MyClass")
    
    # Generation-related methods
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

    def generations_generator(self, num_of_generations: int, is_ghost_mode: bool = True):
        """
        Returns a generator for accessing each generation as the cells evolve
        """
        border_sides = "┊{}┊".format
        border_top = f"╭{"┈┈" * self._curr_gen.cols}╮"
        border_bottom = f"╰{"┈┈" * self._curr_gen.cols}╯"

        for _ in range(0, num_of_generations):
            self._get_next_generation()
            next_gen = (
                self._combine_all_gens_as_str()
                if is_ghost_mode
                else self._curr_gen.as_str
            )
            
            # Add border - TODO: turn into option?
            next_gen_w_side_borders = '\n'.join(border_sides(line) for line in next_gen.split('\n'))
            next_gen_w_all_borders = "{}\n{}\n{}".format(border_top, next_gen_w_side_borders, border_bottom)
            
            yield next_gen_w_all_borders

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
            self._priority_order
        )[combined_matrix].tolist()

        as_str = "\n".join(["".join(row) for row in combined_matrix_cell_states])

        return as_str

    def _cell_to_priority(self, value: str) -> int:
        """
        Maps a cell state value to its priority over other cell states values

        Priority = (lowest -> highest / dead -> alive)
        """
        priority = -1  # assume not in list

        if value in self._priority_order:
            priority = self._priority_order.index(value)

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
