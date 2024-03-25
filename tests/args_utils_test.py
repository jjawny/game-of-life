from src.utils.args_utils import get_cli_args


def test_get_cli_args_success():
    args = get_cli_args()
    expected_args_key = {
        "cols",
        "rows",
        "random",
        "num_of_generations",
        "updates_per_s",
        "is_ghost_mode",
        "is_wrap_mode",
        "survival_rule",
        "resurrection_rule",
        "neighbourhood",
        "radius",
    }

    assert isinstance(args, dict)
    assert set(args.keys()) == expected_args_key
