from src.utils.string_utils import get_banner
from src.models.setting import Setting
import curses
import re


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

    _SPACEBARS_TO_EXIT: int = 2
    _TABS_TO_RESET: int = 2
    _spacebar_count: int = 0
    _tab_count: int = 0
    _cursor_idx: int = 0
    _possible_value_indx: int = 0
    _max_temporary_input_len: int = 20
    _temporary_input: str = ""

    def __init__(
        self,
        settings: list[Setting] | None = None,
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
        is_confirmed = self._spacebar_count >= self._SPACEBARS_TO_EXIT
        is_not_editing = self._temporary_input.strip() == ""
        is_all_values_valid = all(opt.is_value_valid() for opt in self._settings)

        return is_confirmed and is_all_values_valid and is_not_editing

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
            self._render_settings_section(screen)
            self._render_footer(screen)
            screen.refresh()

            self._on_press(key=screen.getch())  # listen

    def _render_banner(self, screen: curses.window):
        menu_width = 46
        screen.addstr("\n\n" + get_banner(menu_width) + "\n\n")

    def _render_settings_section(self, screen: curses.window):
        """
        - Highlights the selected settings
        - Displays disabled settings
        - Displays invalid settings
        - Displays edited settings
        """
        screen.addstr(
            "╭┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈·┈┈┈┈┈·┈ ┈┈ ┈ · ··\n", self._DISABLED_COLOR
        )

        opt_value_l_padding = 40

        for idx, opt in enumerate(self._settings):
            display_setting = f"{opt.display_name}: {str(opt.value).rjust(opt_value_l_padding - len(opt.display_name))}"
            is_selected_setting = idx == self._cursor_idx
            style = curses.A_NORMAL

            if is_selected_setting:
                style |= curses.A_REVERSE

            if is_selected_setting and self._temporary_input.strip():
                style |= self._EDIT_COLOR
                new_display_name = f"* {opt.display_name}"
                display_setting = f"{new_display_name}: {self._temporary_input.rjust(opt_value_l_padding - len(new_display_name))}"
            elif self._is_disabled(opt):
                style |= self._DISABLED_COLOR
            elif not opt.is_value_valid():
                style |= self._ERROR_COLOR

            screen.addstr("┊ ", self._DISABLED_COLOR)  # side border
            screen.addstr(f"{display_setting}\n", style)

        screen.addstr(
            "╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈·┈┈┈┈ ┈┈ · ┈ · ·\n", self._DISABLED_COLOR
        )

    def _render_footer(self, screen: curses.window):
        """Renders the footer"""
        center_len = 44

        # Setting's helper message
        selected_opt_helper_text = self._settings[self._cursor_idx].helper_text
        screen.addstr(f"{selected_opt_helper_text}".center(center_len))
        screen.addstr("\n")

        # Fixed setting options helper message
        options_msg = "LEFT/RIGHT to see options"

        if self.selected_setting.possible_values:
            screen.addstr(options_msg.center(center_len), self._DISABLED_COLOR)
            screen.addstr("\n")
        else:
            screen.addstr("\n")

        # Start helper message
        editing_msg = "Finish editing to start"
        warning_msg = "Please fix errors to start"
        start_msg = "SPACE + SPACE to start"

        if self._temporary_input.strip():
            screen.addstr(editing_msg.center(center_len), self._EDIT_COLOR)
        elif any(not opt.is_value_valid() for opt in self._settings):
            screen.addstr(warning_msg.center(center_len), self._ERROR_COLOR)
        else:
            if self._spacebar_count == 1:
                screen.addstr(start_msg.center(center_len))
            else:
                screen.addstr(start_msg.center(center_len), self._DISABLED_COLOR)

        screen.addstr("\n")

        # Reset helper message
        reset_msg = "TAB + TAB to reset"
        if self._tab_count == 1:
            screen.addstr(reset_msg.center(center_len))
        else:
            screen.addstr(reset_msg.center(center_len), self._DISABLED_COLOR)
        screen.addstr("\n")

        # Exit helper message
        exit_msg = "Ctrl + C to exit"

        screen.addstr(exit_msg.center(center_len), self._DISABLED_COLOR)
        screen.addstr("\n")

    def _on_press(self, key: int):
        """
        Handler for all key presses
            - ⬅️ ➡️: If the selected setting has fixed options, cycles through
            - ⬆️ ⬇️: Navigates through settings (temporary input is cleared)
            - DELETE: Clears the temporary input
            - ENTER: Applies the temporary input to the selected setting
            - SPACE+SPACE: Exits the menu loop
            - R+R: Resets all settings to default option
            - APHANUM: For temporary input
        """
        selected_setting = self.selected_setting
        num_of_settings = len(self._settings)
        num_of_fixed_options = len(selected_setting.possible_values)
        is_fixed_options = True if selected_setting.possible_values else False
        is_valid_input = (
            lambda key: isinstance(key, str)
            and re.match(r"^[a-zA-Z0-9,]+$", key) is not None
        )

        # SPACES: Always handle
        if key == ord(" "):
            self._spacebar_count += 1
        else:
            self._spacebar_count = 0

        # TABS: Always handle
        if key == ord("\t"):
            self._tab_count += 1
        else:
            self._tab_count = 0

        if self._tab_count >= self._TABS_TO_RESET:
            [s.reset_to_default() for s in self._settings]
            self._tab_count = 0

        match key:
            # ARROW KEYS
            case curses.KEY_UP:
                self._clear_temporary_input()
                self._cursor_idx = (self._cursor_idx - 1) % num_of_settings
            case curses.KEY_DOWN:
                self._clear_temporary_input()
                self._cursor_idx = (self._cursor_idx + 1) % num_of_settings
            case curses.KEY_LEFT:
                if is_fixed_options:
                    next_idx = (self._possible_value_indx - 1) % num_of_fixed_options
                    self._possible_value_indx = next_idx
                    self._temporary_input = selected_setting.possible_values[next_idx]
            case curses.KEY_RIGHT:
                if is_fixed_options:
                    next_idx = (self._possible_value_indx + 1) % num_of_fixed_options
                    self._possible_value_indx = next_idx
                    self._temporary_input = selected_setting.possible_values[next_idx]
            # DELETE KEYS
            case 127 | curses.KEY_DC | curses.KEY_BACKSPACE:
                if not is_fixed_options:
                    self._clear_temporary_input()
                    selected_setting.value = ""
            # ENTER KEYS
            case 10 | 13 | curses.KEY_ENTER:
                if self._temporary_input:
                    selected_setting.value = self._temporary_input
                    self._clear_temporary_input()
            # ALPHANUM INPUT
            case _:
                if not is_fixed_options and is_valid_input(chr(key)):
                    if len(self._temporary_input) < self._max_temporary_input_len:
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

    def _is_disabled(self, setting: Setting) -> bool:
        """
        Handles logic for determining if a setting is disabled (ignored) due to other settings
        """

        # Random is disabled by seed that has any value other than "none"
        if setting.name.lower() == "random":
            seed_setting = next((s for s in self._settings if s.name == "seed"), None)
            is_using_seed = seed_setting and isinstance(seed_setting.value, str) and str(seed_setting.value).strip().lower() not in ["none", ""]
            
            if is_using_seed:
                return True

        return False
