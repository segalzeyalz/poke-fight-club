from unittest.mock import Mock

from app.battle_logic import BattleSimulation
from app.models import Pokemon


def test_battle_simulation_creates_detailed_log():
    # Create test Pokemon
    pokemon1 = Pokemon(
        id=1,
        name="Charizard",
        hp=100,
        attack=84,
        defense=78,
        special_attack=109,
        special_defense=85,
        speed=100,
        types=['fire', 'flying'],
        moves=['flamethrower']
    )

    pokemon2 = Pokemon(
        id=2,
        name="Venusaur",
        hp=100,
        attack=82,
        defense=83,
        special_attack=100,
        special_defense=100,
        speed=80,
        types=['grass', 'poison'],
        moves=['solar-beam']
    )

    # Setup battle simulation with mocked services
    mock_type_effectiveness = Mock()
    mock_type_effectiveness.get_type_effectiveness.return_value = 2.0

    mock_move_handler = Mock()
    mock_move_handler.select_move.return_value = 'test-move'
    mock_move_handler.get_move_data.return_value = {
        'name': 'test-move',
        'power': 50,
        'type': 'normal',
        'damage_class': 'physical'
    }

    battle_sim = BattleSimulation(mock_type_effectiveness, mock_move_handler)

    # Run battle simulation
    winner, log = battle_sim.simulate_battle(pokemon1, pokemon2)

    # Verify log contains expected entries
    assert len(log) == 1, "after one hit the HP of pokemon 2 is -1, so the battle should end"
    assert winner == "Charizard", "Charizard should win the battle because Venusaur's HP is -1 after one hit"
