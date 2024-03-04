from src.models.setting import Setting
from src.utils.terminal_utils import print_banner, clear_screen
from src.enums.color import Color
from pynput import keyboard
from typing import Callable
from time import sleep


class MainMenu:
    """
    The main menu
    """

    _SPACEBARS_TO_EXIT = 2
    _num_of_consecutive_spacebar_presses = 0
    _temporary_input: str = ""
    _cursor_idx = 0
    _possible_option_indx = 0
    _example_option = Setting(
        display_name="Look at me!",
        name="arg",
        value=True,
        parse_value_callback=(lambda _: True),
    )

    def __init__(
        self,
        final_callback: Callable[[list[Setting]], None],
        options: list[Setting] = [],
    ):
        self._final_callback = final_callback
        self._options = options if options else [self._example_option]

    @property
    def selected_option(self) -> Setting:
        """Returns the selected option obj"""
        return self._options[self._cursor_idx]

    def render(self):
        self._render()  # initial render

        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:  # type: ignore
            listener.join()

        self._final_callback(self._options)

    def _render(self):
        clear_screen()
        print_banner(offset=23)
        print("╭┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈·┈┈┈┈┈·┈ ┈┈ ┈ · ··")
        self._render_options()
        print("╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈·┈┈┈┈ ┈┈ · ┈ · ·")

    def _on_press(self, key):
        """
        Handler for all key presses
            - Manages state (temporary input, setting values)
            - If the selected setting has fixed options, cycles through (<-, ->)
            - All other selected settings accept alphanumeric inputs
            - Temporary input is cleared when deleting or navigating to other settings (up, down)
            - Press enter to apply the temporary input to the selected setting
        """
        selected_option = self.selected_option
        num_of_options = len(self._options)
        num_of_fixed_options = len(selected_option.possible_values)
        is_fixed_options = True if selected_option.possible_values else False
        is_alphanumeric = (
            lambda key: key is not None and hasattr(key, "char") and key.char.isalnum()
        )

        match key:
            case keyboard.Key.ctrl:
                sleep(0.25)  # Give buffer time to Ctrl+C out
            case keyboard.Key.up:
                self._clear_temporary_input()
                self._cursor_idx = (self._cursor_idx - 1) % num_of_options
            case keyboard.Key.down:
                self._clear_temporary_input()
                self._cursor_idx = (self._cursor_idx + 1) % num_of_options
            case keyboard.Key.left:
                if is_fixed_options:
                    next_idx = (self._possible_option_indx - 1) % num_of_fixed_options
                    self._possible_option_indx = next_idx
                    self._temporary_input = selected_option.possible_values[next_idx]
            case keyboard.Key.right:
                if is_fixed_options:
                    next_idx = (self._possible_option_indx + 1) % num_of_fixed_options
                    self._possible_option_indx = next_idx
                    self._temporary_input = selected_option.possible_values[next_idx]
            case keyboard.Key.enter:
                if self._temporary_input:
                    selected_option.value = self._temporary_input
                    self._clear_temporary_input()
            case keyboard.Key.backspace | keyboard.Key.delete:
                if not is_fixed_options:
                    self._clear_temporary_input()
                    selected_option.value = ""
            case _:
                if not is_fixed_options and is_alphanumeric(key):
                    self._temporary_input += key.char
                    self._temporary_input.strip()

        self._render()  # re-render to reflect changes

    def _on_release(self, key):
        """
        Handler for all key releases:
            - 'Space + Space' to exit the menu loop and execute main callback
        """

        # Record spacebar presses
        if key == keyboard.Key.space:
            self._num_of_consecutive_spacebar_presses += 1
        else:
            self._num_of_consecutive_spacebar_presses = 0

        # Key handling logic
        match key:
            case keyboard.Key.space:
                if (
                    self._num_of_consecutive_spacebar_presses >= self._SPACEBARS_TO_EXIT
                    and self._parse_all_setting_values()
                ):
                    return False  # Stop the listener
            case _:
                pass

    def _clear_temporary_input(self):
        """Explicitly the temporary input"""
        self._temporary_input = ""

    def _render_options(self):
        """
        - Highlights the selected option
        - Displays disabled options as GRAY
        - Displays invalid options as RED
        - Priority highest to lowest: disabled, invalid
        """
        option_format = "┊ {}".format

        for idx, opt in enumerate(self._options):
            opt_to_display = f"{opt.display_name}: {opt.value}"
            is_selected_setting = idx == self._cursor_idx
            bg = Color.BG_HIGHLIGHT if is_selected_setting else None
            fg = None

            if self._is_disabled(opt):
                fg = Color.FG_DISABLED
            elif not opt.is_value_valid():
                fg = Color.FG_ERROR

            # Unsaved changes
            if is_selected_setting and self._temporary_input:
                if self._temporary_input:
                    opt_to_display = f"* {opt.display_name}: {self._temporary_input}"

            print(option_format(self._color_str(opt_to_display, bg, fg)))

    def _color_str(
        self, string: str, bg: Color | None = None, fg: Color | None = None
    ) -> str:
        """
        - Formats a string w colors in the terminal
        - If colors aren't given, will use default terminal colors
        """

        res = ""

        if bg:
            res += bg.value

        if fg:
            res += fg.value

        res += string
        res += Color.RESET.value

        return res

    def _parse_all_setting_values(self) -> bool:
        is_all_successful = True

        # Attempt to parse all
        for setting in self._options:
            if not setting.parse_value():
                is_all_successful = False

        return is_all_successful

    def _is_disabled(self, opt: Setting) -> bool:
        """
        Handles logic for determining if an option is disabled due to other options
        """

        # random is disabled by seed
        # updates_per_s is disabled by step
        return False
