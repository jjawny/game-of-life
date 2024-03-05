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
        default_value,
        parse_value_callback: Callable,
        possible_values: list = [],
        helper_text: str = "",
    ):
        self._display_name = display_name
        self._name = name
        self._value = value
        self._default_value = default_value
        self._parse_value_callback = parse_value_callback
        self._possible_values = possible_values
        self._helper_text = helper_text

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def helper_text(self) -> str:
        return self._helper_text

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
    def value(self, new_value) -> None:
        self._value = new_value

    def is_value_valid(self):
        """Check if the value is able to be parsed without re-assigning"""
        res = self._parse_value_callback(self._value)
        return True if res is not None else False

    def reset_to_default(self):
        """Resets to the default value"""
        self._value = self._default_value

    def parse_value(self) -> bool:
        """
        Attempts to parse and re-assign the current value

        True if success, false otherwise
        """
        is_success = False

        if self.is_value_valid():
            self._value = self._parse_value_callback(self._value)
            is_success = True

        return is_success
