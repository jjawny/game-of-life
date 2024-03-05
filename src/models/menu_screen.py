from src.utils.terminal_utils import get_banner
from src.models.setting import Setting
import curses


class MenuScreen:
    """
    SUMMARY:
        - The main menu, built with curses module
        - Will render its given settings
        - Show() displays the screen, listens for key events, and returns the updated settings

    NOTE:
        - This screen uses the 256 color range ∴ your terminal must be a 256-color terminal
        - Check TERM environment variable, example: 'xterm-256color'
    """

    _SPACEBARS_TO_EXIT = 2
    _num_of_consecutive_spacebars = 0
    _temporary_input: str = ""

    _cursor_idx = 0
    _possible_value_indx = 0

    def __init__(
        self,
        settings: list[Setting] = [],
    ):
        if settings:
            self._settings = settings
        else:
            # Show an example
            self._settings = [
                Setting(
                    display_name="Look at me !",
                    name="key_name",
                    value="no",
                    default_value="yes",
                    possible_values=["yes", "no"],
                    parse_value_callback=(lambda _: "yes"),
                    helper_text="Some very helpful text",
                )
            ]

    @property
    def selected_setting(self) -> Setting:
        return self._settings[self._cursor_idx]

    def show(self):
        """
        SHOW SCREEN:
            - Blocks thread til exit
            - Lists settings ready to be modified
            - Listens to key events
            - SPACE+SPACE: to exit
            - Upon exiting, returns the updated settings
        """
        curses.wrapper(self._render_screen)
        self._parse_all_setting_values()
        return self._settings

    def _is_final_callback_ready(self):
        """Confirms the settings are ready to inject into final callback"""
        is_confirmed = self._num_of_consecutive_spacebars >= self._SPACEBARS_TO_EXIT
        is_all_values_valid = all(opt.is_value_valid() for opt in self._settings)

        return is_confirmed and is_all_values_valid

    def _render_screen(self, screen: curses.window):
        """
        Call with Curses wrapper to inject curses std screen obj (stdscr)
        """

        # Init curses and colors
        curses.use_default_colors()  # !important
        screen.scrollok(True)

        COLOR_GRAY = 244
        COLOR_DEFAULT = -1
        curses.init_pair(1, curses.COLOR_RED, COLOR_DEFAULT)
        curses.init_pair(2, curses.COLOR_YELLOW, COLOR_DEFAULT)
        curses.init_pair(3, COLOR_GRAY, COLOR_DEFAULT)
        self._ERROR_COLOR = curses.color_pair(1)
        self._EDIT_COLOR = curses.color_pair(2)
        self._DISABLED_COLOR = curses.color_pair(3)

        while not self._is_final_callback_ready():
            screen.clear()
            self._render_banner(screen)
            self._render_options_section(screen)
            self._render_footer(screen)
            screen.refresh()

            self._on_press(key=screen.getch())  # listen

    def _render_banner(self, screen: curses.window):
        screen.addstr("\n\n" + get_banner(offset=23) + "\n\n")

    def _render_options_section(self, screen: curses.window):
        """
        - Highlights the selected option
        - Displays disabled options
        - Displays invalid options
        - Displays edited options
        """
        screen.addstr(
            "╭┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈·┈┈┈┈┈·┈ ┈┈ ┈ · ··\n", self._DISABLED_COLOR
        )

        opt_value_l_padding = 40

        for idx, opt in enumerate(self._settings):
            opt_to_display = f"{opt.display_name}: {str(opt.value).rjust(opt_value_l_padding - len(opt.display_name))}"
            is_selected_setting = idx == self._cursor_idx
            style = curses.A_NORMAL

            if is_selected_setting:
                style |= curses.A_REVERSE

            if is_selected_setting and self._temporary_input:
                style |= self._EDIT_COLOR
                new_display_name = f"* {opt.display_name}"
                opt_to_display = f"{new_display_name}: {self._temporary_input.rjust(opt_value_l_padding - len(new_display_name))}"
            elif self._is_disabled(opt):
                style |= self._DISABLED_COLOR
            elif not opt.is_value_valid():
                style |= self._ERROR_COLOR

            screen.addstr("┊ ", self._DISABLED_COLOR)  # side border
            screen.addstr(f"{opt_to_display}\n", style)

        screen.addstr(
            "╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈·┈┈┈┈ ┈┈ · ┈ · ·\n", self._DISABLED_COLOR
        )

    def _render_footer(self, screen: curses.window):
        """Renders the footer"""

        selected_opt_helper_text = self._settings[self._cursor_idx].helper_text
        warning_msg = "Please fix errors to start"
        start_msg = "Space + Space to start"
        exit_msg = "Ctrl + C to exit"
        center_len = 44

        screen.addstr(f"{selected_opt_helper_text}".center(center_len))
        screen.addstr("\n")

        if any(not opt.is_value_valid() for opt in self._settings):
            screen.addstr(warning_msg.center(center_len), self._ERROR_COLOR)
        else:
            screen.addstr(start_msg.center(center_len), self._DISABLED_COLOR)

        screen.addstr("\n")
        screen.addstr(exit_msg.center(center_len), self._DISABLED_COLOR)
        screen.addstr("\n")

    def _on_press(self, key: int):
        """
        Handler for all key presses
            - ⬅️ ➡️: If the selected setting has fixed options, cycles through
            - ⬆️ ⬇️: Navigate through settings (temporary input is cleared)
            - DELETE: Temporary input is cleared
            - ENTER: Applies the temporary input to the selected setting
            - SPACE+SPACE: to exit the menu loop
            - APHANUM: For temporary input
        """
        selected_option = self.selected_setting
        num_of_options = len(self._settings)
        num_of_fixed_options = len(selected_option.possible_values)
        is_fixed_options = True if selected_option.possible_values else False
        is_alphanumeric = lambda key: isinstance(key, str) and key.isalnum()

        # SPACE: Handle separately
        if key == 32:
            self._num_of_consecutive_spacebars += 1
        else:
            self._num_of_consecutive_spacebars = 0

        match key:
            # ARROW KEYS
            case curses.KEY_UP:
                self._clear_temporary_input()
                self._cursor_idx = (self._cursor_idx - 1) % num_of_options
            case curses.KEY_DOWN:
                self._clear_temporary_input()
                self._cursor_idx = (self._cursor_idx + 1) % num_of_options
            case curses.KEY_LEFT:
                if is_fixed_options:
                    next_idx = (self._possible_value_indx - 1) % num_of_fixed_options
                    self._possible_value_indx = next_idx
                    self._temporary_input = selected_option.possible_values[next_idx]
            case curses.KEY_RIGHT:
                if is_fixed_options:
                    next_idx = (self._possible_value_indx + 1) % num_of_fixed_options
                    self._possible_value_indx = next_idx
                    self._temporary_input = selected_option.possible_values[next_idx]
            # DELETE KEYS
            case 127 | curses.KEY_DC | curses.KEY_BACKSPACE:
                if not is_fixed_options:
                    self._clear_temporary_input()
                    selected_option.value = ""
            # ENTER KEYS
            case 10 | 13 | curses.KEY_ENTER:
                if self._temporary_input:
                    selected_option.value = self._temporary_input
                    self._clear_temporary_input()
            # ALPHANUM INPUT
            case _:
                if not is_fixed_options and is_alphanumeric(chr(key)):
                    self._temporary_input += chr(key)
                    self._temporary_input.strip()

    def _clear_temporary_input(self):
        """Explicitly the temporary input"""
        self._temporary_input = ""

    def _parse_all_setting_values(self) -> bool:
        """
        - Attempts to parse all settings, even if some fail
        - Returns true if all succeeded, false otherwise
        """
        is_all_successful = True

        for setting in self._settings:
            if not setting.parse_value():
                is_all_successful = False

        return is_all_successful

    def _is_disabled(self, opt: Setting) -> bool:
        """
        Handles logic for determining if an option is disabled (ignored) due to other options
        """

        # if opt.name == "random" and self._options:

        # random is disabled by seed
        # updates_per_s is disabled by step
        return False
