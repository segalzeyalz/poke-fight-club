import pytest
from unittest.mock import Mock
from app.services.pokeapi_service import PokeAPIService
from app.models import PokemonData
from app.exceptions import (
    PokemonNotFoundException,
    PokemonAPIException,
    MoveNotFoundException,
)

@pytest.fixture
def service():
    return PokeAPIService(
        cache_manager=Mock(),
        url_mapper=Mock(),
        api_client=Mock(),
        data_transformer=Mock()
    )

def test_get_pokemon_data_from_cache(service):
    service.cache_manager.get_pokemon_data.return_value = {'cached': True}

    result = service.get_pokemon_data('pikachu')

    assert result == {'cached': True}
    service.api_client.get.assert_not_called()

def test_get_pokemon_data_from_api(service):
    # Arrange
    service.cache_manager.get_pokemon_data.return_value = None
    service.url_mapper.get_pokemon_url.return_value = 'pokemon/pikachu'
    service.api_client.get.return_value = {'raw': 'data'}
    service.data_transformer.transform_to_pokemon_data.return_value = PokemonData(
        id=25, name='pikachu', stats={}, types=[], moves=[]
    )

    result = service.get_pokemon_data('pikachu')

    assert isinstance(result, PokemonData)
    service.cache_manager.set_pokemon_data.assert_called_once()

def test_get_pokemon_data_not_found(service):
    service.cache_manager.get_pokemon_data.return_value = None
    service.url_mapper.get_pokemon_url.side_effect = PokemonNotFoundException('pikachu')

    with pytest.raises(PokemonNotFoundException):
        service.get_pokemon_data('pikachu')

def test_get_move_data_empty_name(service):
    with pytest.raises(ValueError, match="Move name cannot be empty"):
        service.get_move_data("")

def test_get_move_data_from_cache(service):
    service.cache_manager.get_move_data.return_value = {'cached': True}

    result = service.get_move_data('thunder')

    assert result == {'cached': True}
    service.api_client.get.assert_not_called()

def test_get_move_data_from_api(service):
    service.cache_manager.get_move_data.return_value = None
    service.api_client.get.return_value = {
        'name': 'thunder',
        'power': 110,
        'type': {'name': 'electric'},
        'damage_class': {'name': 'special'}
    }

    result = service.get_move_data('thunder')

    expected_result = {
        'name': 'thunder',
        'power': 110,
        'type': 'electric',
        'damage_class': 'special'
    }
    assert result == expected_result
    service.cache_manager.set_move_data.assert_called_once_with('thunder', expected_result)

def test_get_move_data_not_found(service):
    service.cache_manager.get_move_data.return_value = None
    mock_error = PokemonAPIException("Not found")
    setattr(mock_error, 'status_code', 404)
    service.api_client.get.side_effect = mock_error

    with pytest.raises(MoveNotFoundException):
        service.get_move_data('not-exists')

def test_transform_pokemon_data(service):
    mock_data = PokemonData(id=25, name='pikachu', stats={}, types=[], moves=[])
    mock_pokemon = Mock(id=25, name='pikachu')
    service.data_transformer.transform_to_pokemon.return_value = mock_pokemon

    result = service.transform_pokemon_data(mock_data)

    assert result == mock_pokemon
    service.data_transformer.transform_to_pokemon.assert_called_once_with(mock_data)
