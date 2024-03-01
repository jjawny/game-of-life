from src.constants import constants


class Settings:
    """
    Holds the state for general simulation settings.
    Grid-specific settings are stored in the Grid instance's state
    """

    def __init__(self, generations: int = constants.DEFAULT_GENERATIONS):
        self._generations: int = generations

    @property
    def generations(self):
        return self._generations
