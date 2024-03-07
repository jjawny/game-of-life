from src.models.simulation_screen import SimulationScreen
from src.utils.settings_utils import get_settings
from src.models.cell_matrix import CellMatrix
from src.models.menu_screen import MenuScreen
from src.utils.args_utils import get_cli_args
from src.utils.seed_utils import get_seed
from src.models.setting import Setting


def setup_matrix(settings: list[Setting]) -> CellMatrix:
    """Setup the matrix w settings"""

    # Convert to dict for easy assignment
    settings_dict = {setting.name: setting.value for setting in settings}
    matrix = CellMatrix(
        seed=get_seed(settings_dict["seed"]),
        cols=settings_dict["cols"],
        rows=settings_dict["rows"],
        random=settings_dict["random"],
        is_wrap=settings_dict["is_wrap_mode"],
        survival_rule=settings_dict["survival_rule"],
        resurrection_rule=settings_dict["resurrection_rule"],
        neighbourhood=settings_dict["neighbourhood"],
        radius=settings_dict["radius"],
    )
    
    return matrix


def main() -> None:
    """Extracted main method to be optionally triggered by another script"""
    try:
        initial_settings = get_settings(get_cli_args())
        settings = MenuScreen(settings=initial_settings).show()

        initial_gen = setup_matrix(settings=settings)
        is_ghost_mode = next((s.value for s in settings if s.name == "is_ghost_mode"), True)
        num_of_generations = next((s.value for s in settings if s.name == "num_of_generations"), 100)
        updates_per_s = next((s.value for s in settings if s.name == "updates_per_s"), 10)

        simulation = SimulationScreen(initial_gen=initial_gen, is_ghost_mode=is_ghost_mode, num_of_generations=num_of_generations, updates_per_s=updates_per_s)
        all_gens = simulation.show()

        if all_gens:
            print(f"\n{all_gens[-1]}")

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as ex:
        print("\nAn unexpected error has occurred...", ex)
    finally:
        print("")
