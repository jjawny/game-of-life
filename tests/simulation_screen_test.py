from src.models.simulation_screen import SimulationScreen
import pytest


@pytest.fixture
def mock_model() -> SimulationScreen:
    return SimulationScreen()


def test_generations_generator_success(mock_model):
    NUM_OF_GENERATIONS = 10
    generator = mock_model.generations_generator(NUM_OF_GENERATIONS)
    count_to_assert = 0

    for _ in generator:
        count_to_assert += 1

    assert count_to_assert == NUM_OF_GENERATIONS
