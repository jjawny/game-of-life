from src.constants import constants


class Grid:
    def __init__(self, width=constants.DEFAULT_WIDTH, height=constants.DEFAULT_HEIGHT):
        self._rows = width
        self._cols = height

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols
