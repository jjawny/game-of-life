import numpy as np
import curses
import math

from src.utils.string_utils import get_banner
from src.models.cell_matrix import CellMatrix
from src.enums.cell_state import CellState
from time import sleep
from copy import copy


class SimulationScreen:
    # Generations
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

    _final_gen = ""

    def __init__(self, num_of_generations: int = 100, is_ghost_mode: bool = True, updates_per_s: int = 10, initial_gen: CellMatrix = CellMatrix()):
        self._num_of_generations = num_of_generations
        self._is_ghost_mode = is_ghost_mode
        self._updates_per_s = updates_per_s
        self._curr_gen = initial_gen

    @property
    def curr_gen(self):
        """Returns the current generation's cell matrix"""
        return self._curr_gen

    def show(self):
        """
        SHOW SCREEN:
            - Blocks thread til exit
            - Starts simulation
            - Exists when simulation ends
            - Returns the final generation as a string
        """
        curses.wrapper(self._render_screen)
        return self._final_gen
    
    def _render_screen(self, screen: curses.window):
        """
        Call with Curses wrapper to inject curses std screen obj (stdscr)
        """

        # Init curses and colors
        curses.use_default_colors()  # !important
        screen.scrollok(True)

        screen.clear()

        generations = self.generations_generator(self._num_of_generations, self._is_ghost_mode)
        delay_s = 1 / self._updates_per_s
        offset = math.floor(len(self.curr_gen.as_str.split("\n")[0]) / 2)

        line_width = len(self.curr_gen.as_str.split("\n")[0])

        self._render_banner(screen, offset)
        screen.addstr(self.curr_gen.as_str)
        self._render_footer(screen, 1, line_width)

        for idx, gen in enumerate(generations):
            sleep(delay_s)
            screen.clear()
            self._render_banner(screen, offset)
            screen.addstr(gen)
            screen.addstr("\n")
            self._render_footer(screen, idx + 1, line_width)
            screen.refresh()
            self._final_gen = gen

        screen.addstr("Press any key to exit".center(line_width))
        screen.addstr("\n")
        screen.getkey() # block until key press

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

    def _render_footer(self, screen: curses.window, idx: int, line_width: int = 0):
        """Renders the footer"""
        screen.addstr(f"Generation #{idx}".center(line_width))
        screen.addstr("\n")
    
    def _render_banner(self, screen: curses.window, offset: int = 0):
        screen.addstr("\n\n" + get_banner(offset) + "\n\n")

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
