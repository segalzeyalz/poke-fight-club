import pytest
import requests
from unittest.mock import Mock, patch
from app.services.url_map_service import PokemonURLMapper
from app.exceptions import PokemonAPIException, PokemonNotFoundException


@pytest.fixture
def cache_manager():
    return Mock()


@pytest.fixture
def url_mapper(cache_manager):
    return PokemonURLMapper(cache_manager)


def test_initialize_mapping_from_cache(cache_manager):
    # Arrange
    cached_mapping = {
        'pikachu': 'https://pokeapi.co/api/v2/pokemon/25'
    }
    cache_manager.get_pokemon_data.return_value = cached_mapping

    # Act
    mapper = PokemonURLMapper(cache_manager)

    # Assert
    assert mapper.pokemon_urls == cached_mapping
    cache_manager.get_pokemon_data.assert_called_once_with('pokemon_url_mapping')


def test_initialize_mapping_from_api(cache_manager):
    # Arrange
    cache_manager.get_pokemon_data.return_value = None
    mock_response = Mock()
    mock_response.json.return_value = {
        'results': [
            {'name': 'pikachu', 'url': 'https://pokeapi.co/api/v2/pokemon/25'}
        ],
        'next': None
    }
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response) as mock_get:
        # Act
        mapper = PokemonURLMapper(cache_manager)

        # Assert
        assert mapper.pokemon_urls == {
            'pikachu': 'https://pokeapi.co/api/v2/pokemon/25'
        }
        cache_manager.set_pokemon_data.assert_called_once()
        mock_get.assert_called()


def test_get_pokemon_url_success(url_mapper):
    # Arrange
    url_mapper.pokemon_urls = {
        'pikachu': 'https://pokeapi.co/api/v2/pokemon/25'
    }

    # Act
    url = url_mapper.get_pokemon_url('pikachu')

    # Assert
    assert url == 'https://pokeapi.co/api/v2/pokemon/25'


def test_get_pokemon_url_not_found(url_mapper):
    # Arrange
    url_mapper.pokemon_urls = {}

    # Act/Assert
    with pytest.raises(PokemonNotFoundException):
        url_mapper.get_pokemon_url('not-exists')


def test_get_pokemon_url_case_insensitive(url_mapper):
    # Arrange
    url_mapper.pokemon_urls = {
        'pikachu': 'https://pokeapi.co/api/v2/pokemon/25'
    }

    # Act
    url = url_mapper.get_pokemon_url('PIKACHU')

    # Assert
    assert url == 'https://pokeapi.co/api/v2/pokemon/25'


def test_make_api_request_timeout():
    # Arrange
    with patch('requests.get', side_effect=requests.Timeout):
        # Act/Assert
        with pytest.raises(PokemonAPIException, match="Request timed out"):
            PokemonURLMapper._make_api_request("https://test-url.com")


def test_make_api_request_error():
    # Arrange
    with patch('requests.get', side_effect=requests.RequestException("Network error")):
        # Act/Assert
        with pytest.raises(PokemonAPIException, match="API request failed: Network error"):
            PokemonURLMapper._make_api_request("https://test-url.com")


def test_fetch_all_pokemon_urls_pagination(cache_manager):
    # Arrange
    cache_manager.get_pokemon_data.return_value = None
    first_response = Mock()
    first_response.json.return_value = {
        'results': [{'name': 'pikachu', 'url': 'url1'}],
        'next': 'next_url'
    }
    second_response = Mock()
    second_response.json.return_value = {
        'results': [{'name': 'charmander', 'url': 'url2'}],
        'next': None
    }

    with patch('requests.get') as mock_get:
        mock_get.side_effect = [first_response, second_response]

        # Act
        mapper = PokemonURLMapper(cache_manager)

        # Assert
        assert mapper.pokemon_urls == {
            'pikachu': 'url1',
            'charmander': 'url2'
        }
        assert mock_get.call_count == 2