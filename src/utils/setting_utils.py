from src.enums.neighbourhood import Neighbourhood
from src.models.setting import Setting
from src.constants import constants


def get_settings(args: dict):
    """Renders the main menu and reads user inputs"""

    # User-friendly values will be converted back to proper value when parsed
    user_friendly_default_neighbourhood = constants.DEFAULT_NEIGHBOURHOOD.value
    user_friendly_neighbourhood = args.get(
        "neighbourhood", constants.DEFAULT_NEIGHBOURHOOD.value
    )

    user_friendly_default_survival_rule = ",".join(
        map(str, constants.DEFAULT_SURVIVAL_RULE)
    )
    user_friendly_survival_rule = args.get(
        "survival_rule", constants.DEFAULT_SURVIVAL_RULE
    )
    if isinstance(user_friendly_survival_rule, set):
        converted = ",".join(map(str, user_friendly_survival_rule))
        user_friendly_survival_rule = converted

    user_friendly_default_resurrection_rule = ",".join(
        map(str, constants.DEFAULT_RESURRECTION_RULE)
    )
    user_friendly_resurrection_rule = args.get(
        "resurrection_rule", constants.DEFAULT_RESURRECTION_RULE
    )
    if isinstance(user_friendly_resurrection_rule, set):
        converted = ",".join(map(str, user_friendly_resurrection_rule))
        user_friendly_resurrection_rule = converted

    # Create the settings w fallback default values
    res: list[Setting] = [
        Setting(
            display_name="Dimension X",
            name="cols",
            value=args.get("cols", constants.DEFAULT_DIMENSION_X),
            default_value=constants.DEFAULT_DIMENSION_X,
            parse_value_callback=parse_dimension,
            helper_text=f"Matrix height/rows {constants.MIN_DIMENSION}..{constants.MAX_DIMENSION} inclusive",
        ),
        Setting(
            display_name="Dimension Y",
            name="rows",
            value=args.get("rows", constants.DEFAULT_DIMENSION_Y),
            default_value=constants.DEFAULT_DIMENSION_Y,
            parse_value_callback=parse_dimension,
            helper_text=f"Matrix width/cols {constants.MIN_DIMENSION}..{constants.MAX_DIMENSION} inclusive",
        ),
        Setting(
            display_name="Random %",
            name="random",
            value=args.get("random", constants.DEFAULT_RANDOM),
            default_value=constants.DEFAULT_RANDOM,
            parse_value_callback=parse_random,
            helper_text=f"Chance for cell to start alive {constants.MIN_RANDOM}..{constants.MAX_RANDOM}% inclusive",
        ),
        Setting(
            display_name="Generations",
            name="num_of_generations",
            value=args.get("num_of_generations", constants.DEFAULT_NUM_OF_GENERATIONS),
            default_value=constants.DEFAULT_NUM_OF_GENERATIONS,
            parse_value_callback=parse_generations,
            helper_text=f"Number of generations {constants.MIN_GENERATIONS}..{constants.MAX_GENERATIONS} inclusive",
        ),
        Setting(
            display_name="Updates per second",
            name="updates_per_s",
            value=args.get("updates_per_s", constants.DEFAULT_UPDATES_PER_S),
            default_value=constants.DEFAULT_UPDATES_PER_S,
            parse_value_callback=parse_updates_per_s,
            helper_text=f"Refresh rate of generations per second {constants.MIN_UPDATES_PER_S}..{constants.MIN_UPDATES_PER_S} inclusive",
        ),
        Setting(
            display_name="Ghost mode",
            name="is_ghost_mode",
            value=args.get("is_ghost_mode", constants.DEFAULT_IS_GHOST_MODE),
            default_value=constants.DEFAULT_IS_GHOST_MODE,
            possible_values=["True", "False"],
            parse_value_callback=parse_bool,
            helper_text="Toggle ghost mode (older generations fading away)",
        ),
        Setting(
            display_name="Wrap mode",
            name="is_wrap_mode",
            value=args.get("is_wrap_mode", constants.DEFAULT_IS_WRAP_MODE),
            default_value=constants.DEFAULT_IS_WRAP_MODE,
            possible_values=["True", "False"],
            parse_value_callback=parse_bool,
            helper_text="Toggle wrap mode (neighbourhoods wrap around matrix bounds)",
        ),
        Setting(
            display_name="Survival rule",
            name="survival_rule",
            value=user_friendly_survival_rule,
            default_value=user_friendly_default_survival_rule,
            parse_value_callback=parse_rule,
            helper_text="Number of alive neighbour cells for (alive) host cell to survive",
        ),
        # NOTE: Use set as string for user-friendly display, will be converted back to set when parsed
        Setting(
            display_name="Resurrection rule",
            name="resurrection_rule",
            value=user_friendly_resurrection_rule,
            default_value=user_friendly_default_resurrection_rule,
            parse_value_callback=parse_rule,
            helper_text="Number of alive neighbour cells for (dead) host cell to resurrect",
        ),
        Setting(
            display_name="Neighbourhood",
            name="neighbourhood",
            value=user_friendly_neighbourhood,
            default_value=user_friendly_default_neighbourhood,
            possible_values=["Moore", "VonNeumann"],
            parse_value_callback=parse_neighbourhood,
            helper_text=f"Neighbourhood type '{Neighbourhood.MOORE.value}' or '{Neighbourhood.VON_NEUMANN.value}'",
        ),
        Setting(
            display_name="Radius",
            name="radius",
            value=args.get("radius", constants.DEFAULT_RADIUS),
            default_value=constants.DEFAULT_RADIUS,
            parse_value_callback=parse_radius,
            helper_text="Size of the neighbourhood",
        ),
    ]

    return res


def parse_dimension(value) -> int | None:
    """Returns the parsed dimension, otherwise None"""
    try:
        if constants.MIN_DIMENSION <= int(value) <= constants.MAX_DIMENSION:
            return int(value)
    except:
        return None


def parse_random(value) -> int | None:
    """Returns the parsed random percentage, otherwise None"""
    try:
        if constants.MIN_RANDOM <= int(value) <= constants.MAX_RANDOM:
            return int(value)
    except:
        return None


def parse_generations(value) -> int | None:
    """Returns the parsed generations count, otherwise None"""
    try:
        if constants.MIN_GENERATIONS <= int(value) <= constants.MAX_GENERATIONS:
            return int(value)
    except:
        return None


def parse_updates_per_s(value) -> int | None:
    """Returns the parsed updates per second count, otherwise None"""
    try:
        if constants.MIN_UPDATES_PER_S <= int(value) <= constants.MAX_UPDATES_PER_S:
            return int(value)
    except:
        return None


def parse_bool(value) -> bool | None:
    """Returns the parsed bool, otherwise None"""
    try:
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
    except:
        return None


def parse_rule(value) -> set | None:
    """Returns the parsed rule, otherwise None"""

    try:
        if isinstance(value, set):
            return value
        elif not isinstance(value, str):
            return None

        strings = [v.strip() for v in value.split(",")]
        res = set()

        for s in strings:
            if not s.isdigit():
                return None
            res.add(int(s))

        return res
    except:
        return None


def parse_neighbourhood(value) -> Neighbourhood | None:
    """Returns the neighbourhood bool, otherwise None"""
    try:
        if not isinstance(value, str):
            return None

        match value.lower():
            case "moore":
                return Neighbourhood.MOORE
            case "vonneumann":
                return Neighbourhood.VON_NEUMANN
            case _:
                return None
    except:
        return None


def parse_radius(value) -> int | None:
    """Returns the parsed radius, otherwise None"""
    try:
        if constants.MIN_RADIUS <= int(value) <= constants.MAX_RADIUS:
            return int(value)
    except:
        return None
