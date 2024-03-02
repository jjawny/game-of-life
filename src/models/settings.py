from src.constants import constants


class Settings:
    """
    Holds the state for general simulation settings.
    Grid-specific settings are stored in the Grid instance's state
    """

    def __init__(
        self,
        generations_count: int = constants.DEFAULT_GENERATIONS,
        updates_per_s: int = constants.DEFAULT_UPDATES_PER_S,
    ):
        self._generations_count: int = generations_count
        self._updates_per_s: int = updates_per_s

    @property
    def generations_count(self):
        return self._generations_count

    @generations_count.setter
    def generations_count(self, generations: int):
        self._generations_count = generations

    @property
    def updates_per_s(self):
        return self._updates_per_s

    @updates_per_s.setter
    def updates_per_s(self, updates_per_s: int):
        self._updates_per_s = updates_per_s
