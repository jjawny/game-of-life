from src.enums.neighbourhood import Neighbourhood
from src.enums.seed import Seed

# Bounds
MIN_GENERATIONS: int = 1
MAX_GENERATIONS: int = 10_000

MIN_UPDATES_PER_S: int = 1
MAX_UPDATES_PER_S: int = 1_000

MIN_DIMENSION: int = 1
MAX_DIMENSION: int = 30

MIN_RULE: int = 1
MAX_RULE: int = 100

MIN_RADIUS: int = 1
MAX_RADIUS: int = 100

MIN_RANDOM: int = 0
MAX_RANDOM: int = 100

# Defaults
DEFAULT_NUM_OF_GENERATIONS: int = 32
DEFAULT_UPDATES_PER_S: int = 8
DEFAULT_DIMENSION_X: int = 16
DEFAULT_DIMENSION_Y: int = 16
DEFAULT_IS_GHOST_MODE: bool = True
DEFAULT_IS_WRAP_MODE: bool = True
DEFAULT_SURVIVAL_RULE: set[int] = {2, 3}
DEFAULT_RESURRECTION_RULE: set[int] = {3}
DEFAULT_RANDOM: int = 50  # %
DEFAULT_NEIGHBOURHOOD: Neighbourhood = Neighbourhood.MOORE
DEFAULT_RADIUS: int = 1
DEFAULT_SEED: Seed = Seed.GLIDER
