import pytest
from unittest.mock import Mock, patch

from app.battle_logic import BattleSimulation
from app.battle_logic.move_handler import MoveHandler
from app.battle_logic.type_effectiveness import TypeEffectiveness
from app.cache.pokemon_cache import PokemonCacheManager
from app.models import Pokemon
from app.services.pokeapi_service import PokeAPIService


def test_get_move_data_success():
    """
    Test the get_move_data method of the PokeAPIService class.
    """
    mock_pokemon_list_response = Mock()
    mock_pokemon_list_response.status_code = 200
    mock_pokemon_list_response.json.return_value = {
        'results': [
            {'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'},
            {'name': 'charmander', 'url': 'https://pokeapi.co/api/v2/pokemon/4/'}
        ],
        'next': None  # No more pages
    }

    mock_move_response = Mock()
    mock_move_response.status_code = 200
    mock_move_response.json.return_value = {
        'name': 'tackle',
        'power': 40,
        'type': {'name': 'normal'},
        'damage_class': {'name': 'physical'}
    }

    def mock_get(url):
        if 'pokemon?' in url:
            return mock_pokemon_list_response
        return mock_move_response

    with patch('requests.get', side_effect=mock_get):
        cache_manager = PokemonCacheManager()
        pokeapi_service = PokeAPIService('https://pokeapi.co/api/v2/', cache_manager)
        move_data = pokeapi_service.get_move_data('tackle')

        assert move_data['name'] == 'tackle', "The move name should be 'tackle' as per the test data"
        assert move_data['power'] == 40, "The move power should be 40 as per the test data"
        assert move_data['type'] == 'normal', "The move type should be 'normal' as per the test data"
        assert move_data['damage_class'] == 'physical', "The move damage class should be 'physical' as per the test data"

def test_get_move_data_cached():
    cache_manager = PokemonCacheManager()
    cached_move = {
        'name': 'tackle',
        'power': 40,
        'type': 'normal',
        'damage_class': 'physical'
    }
    cache_manager.set_move_data('tackle', cached_move)

    pokeapi_service = PokeAPIService('https://pokeapi.co/api/v2/', cache_manager)
    move_data = pokeapi_service.get_move_data('tackle')

    assert move_data == cached_move, "The move data should be retrieved from the cache"


def test_get_move_data_api_error():
    mock_response = Mock()
    mock_response.status_code = 404

    with patch('requests.get', return_value=mock_response):
        cache_manager = PokemonCacheManager()
        pokeapi_service = PokeAPIService('https://pokeapi.co/api/v2/', cache_manager)
        with pytest.raises(ValueError):
            pokeapi_service.get_move_data('nonexistent_move')


@pytest.fixture
def mock_pokeapi_service():
    cache_manager = PokemonCacheManager()
    service = PokeAPIService('https://pokeapi.co/api/v2/', cache_manager)

    # Mock the get_move_data method to return test data
    def mock_get_move_data(move_name):
        return {
            'flamethrower': {
                'name': 'flamethrower',
                'power': 90,
                'type': 'fire',
                'damage_class': 'special'
            },
            'solar-beam': {
                'name': 'solar-beam',
                'power': 120,
                'type': 'grass',
                'damage_class': 'special'
            }
        }.get(move_name, {})

    service.get_move_data = mock_get_move_data
    return service


def test_damage_calculation(mock_pokeapi_service):
    attacker = Pokemon(
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

    defender = Pokemon(
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

    move_handler = MoveHandler(mock_pokeapi_service)
    battle_sim = BattleSimulation(TypeEffectiveness(), move_handler)
    damage = battle_sim.calculate_damage(attacker, defender)

    assert damage > 0, "Damage should be greater than 0 because the move is super effective against Grass, special attack is used, and the move has good base power"

    assert damage > 50, "Damage should be high because the move is super effective against Grass, special attack is used, and the move has good base power"