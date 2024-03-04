from typing import Callable


class Setting:
    """
    - Represents a single setting
    - Stores the current value
    - Takes a callback to validate the value
    """

    def __init__(
        self,
        display_name: str,
        name: str,
        value,
        parse_value_callback: Callable,
        possible_values: list = [],
    ):
        self._display_name = display_name
        self._name = name
        self._value = value
        self._parse_value_callback = parse_value_callback
        self._possible_values = possible_values
        # helper text for footer?

    def is_value_valid(self):
        try:
            res = self._parse_value_callback(self._value)
            return True if res is not None else False
        except Exception as _:
            return False

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def possible_values(self) -> list:
        return self._possible_values

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def parse_value(self):
        """
        - Attempts to parse the current value
        - True if success, false otherwise
        """
        try:
            self._value = self._parse_value_callback(self._value)
            return True
        except:
            return False
