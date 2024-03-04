# import math

# from src.utils.terminal_utils import clear_screen, print_banner, print_generation_count_footer
# from src.models.cell_matrix import CellMatrix
# from src.models.game_state import game_state
# from src.enums.cell_state import CellState
# from time import sleep

# # Index = priority (lowest -> highest / dead -> alive)
# priority_state_list = [
#     CellState.DEAD.value,
#     CellState.RARE.value,
#     CellState.MEDIUM.value,
#     CellState.WELL_DONE.value,
#     CellState.ALIVE.value,
# ]

# # State that belongs to a previous generation at the corresponding index (newest -> oldest)
# ghost_state_list = [
#     CellState.WELL_DONE,
#     CellState.MEDIUM,
#     CellState.RARE,
# ]

# def testing_final_callback(opts: dict):
#     """
#     Starts the simulation based on the settings

#     To keep things modular, the following has no knowledge of global 'game_state'

#     TODO: remove game_state from global and instead have these methods as a module? decouple from game_state

#     Throws if unable to find or parse an opt
#     """

#     # TODO: temporarily inject the glider for testing, need to explore regression/unit testing in python
#     glider: list[tuple[int, int]] = [
#         # x, y
#         (0, 2),
#         (1, 1),
#         (2, 1),
#         (2, 2),
#         (2, 3),
#     ]

#     initial_matrix = CellMatrix(
#         seed=glider,
#         cols=opts["cols"],
#         rows=opts["rows"],
#         radius=opts["radius"],
#         random=opts["random"],
#         neighbourhood=opts["neighbourhood"],
#         is_wrap=opts["is_wrap_mode"],
#         survival_rule=opts["survival_rule"],
#         resurrection_rule=opts["resurrection_rule"],
#     )
#     game_state.assign_new_cell_matrix(initial_matrix)


#     # Actual code
#     generations = game_state.generations_generator()
#     delay_s = 1 / game_state.get_value("updates_per_s")

#     # Print initial cells
#     print(game_state.curr_gen.as_str)

#     for idx, gen in enumerate(generations):
#         # keyboard.wait('space') if game_state.is_step_mode: else sleep(delay_s)
#         sleep(delay_s)
#         clear_screen()
#         offset = math.floor(len(gen.split("\n")[0]) / 2)
#         print_banner(offset)
#         print(gen)
#         print_generation_count_footer(idx, offset)

from src.enums.cell_state import CellState


def cell_to_priority(value: str) -> int:
    """
    Maps a cell state value to its priority over other cell states values

    Priority = (lowest -> highest / dead -> alive)
    """

    priority_order = [
        CellState.DEAD.value,
        CellState.RARE.value,
        CellState.MEDIUM.value,
        CellState.WELL_DONE.value,
        CellState.ALIVE.value,
    ]

    priority = -1  # assume not in list

    if value in priority_order:
        priority = priority_order.index(value)

    return priority
