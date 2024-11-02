from typing import Dict, List, Optional
import requests
from pydash import get
from toolz import pipe, curry
from pydantic import ValidationError

from app.config import Config
from app.models import PokemonData, Pokemon
from app.cache.pokemon_cache import PokemonCacheManager
from app.exceptions import (
    PokemonNotFoundException,
    PokemonAPIException,
    MoveNotFoundException,
    InvalidDataException
)


class PokeAPIService:
    def __init__(self, cache_manager: PokemonCacheManager):
        self.base_url = Config.POKEAPI_BASE_URL
        self.cache_manager = cache_manager
        self.pokemon_urls: Dict[str, str] = {}
        self._initialize_pokemon_mapping()

    def _initialize_pokemon_mapping(self) -> None:
        """Initialize the mapping between Pokemon names and their URLs."""
        try:
            cached_mapping = self.cache_manager.get_pokemon_data('pokemon_url_mapping')
            if cached_mapping:
                self.pokemon_urls = cached_mapping
                return

            self._fetch_all_pokemon_urls()
            self.cache_manager.set_pokemon_data('pokemon_url_mapping', self.pokemon_urls)

        except requests.RequestException as e:
            raise PokemonAPIException(f"Failed to connect to PokeAPI: {str(e)}")
        except Exception as e:
            raise PokemonAPIException(f"Failed to initialize Pokemon mapping: {str(e)}")

    def _fetch_all_pokemon_urls(self) -> None:
        """Fetch all Pokemon URLs from the API."""
        url = f'{self.base_url}/pokemon?offset=0&limit=1302'
        all_pokemon = []
        next_url = url

        while next_url:
            response = self._make_api_request(next_url)
            data = response.json()
            all_pokemon.extend(data['results'])
            next_url = data.get('next')

        self.pokemon_urls = {
            pokemon['name']: pokemon['url']
            for pokemon in all_pokemon
        }

    def _make_api_request(self, url: str) -> requests.Response:
        """Make an API request with error handling."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.Timeout:
            raise PokemonAPIException("Request timed out")
        except requests.RequestException as e:
            raise PokemonAPIException(f"API request failed: {str(e)}")

    def get_pokemon_url(self, pokemon_name: str) -> str:
        """Get the URL for a specific Pokemon."""
        pokemon_name = pokemon_name.lower()
        if pokemon_name not in self.pokemon_urls:
            raise PokemonNotFoundException(pokemon_name)
        return self.pokemon_urls[pokemon_name]

    def get_pokemon_data(self, pokemon_name: str) -> PokemonData:
        """Get comprehensive data for a specific Pokemon."""
        cached_data = self.cache_manager.get_pokemon_data(pokemon_name)
        if cached_data:
            return cached_data

        try:
            url = self.get_pokemon_url(pokemon_name)
            response = self._make_api_request(url)
            data = response.json()

            types = list(map(lambda t: t['type']['name'], data.get('types', [])))
            moves = list(map(lambda m: m['move']['name'], data.get('moves', [])))

            pokemon_data = PokemonData(
                id=get(data, 'id'),
                name=get(data, 'name'),
                stats=self._extract_stats(data),
                types=types,
                moves=moves[:4]  # Select first 4 moves
            )

            self.cache_manager.set_pokemon_data(pokemon_name, pokemon_data)
            return pokemon_data

        except ValidationError as e:
            raise InvalidDataException(f"Invalid Pokemon data format: {str(e)}")
        except PokemonNotFoundException:
            raise
        except Exception as e:
            raise PokemonAPIException(f"Failed to get Pokemon data: {str(e)}")

    def get_move_data(self, move_name: str) -> dict:
        """Get data for a specific move."""
        if not move_name:
            raise ValueError("Move name cannot be empty")

        cached_move = self.cache_manager.get_move_data(move_name)
        if cached_move:
            return cached_move

        try:
            url = f'{self.base_url}/move/{move_name}'
            response = self._make_api_request(url)
            move_data = response.json()

            simplified_move_data = {
                'name': get(move_data, 'name'),
                'power': get(move_data, 'power', 0),
                'type': get(move_data, 'type.name'),
                'damage_class': get(move_data, 'damage_class.name')
            }

            self.cache_manager.set_move_data(move_name, simplified_move_data)
            return simplified_move_data

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise MoveNotFoundException(f"Move {move_name} not found")
            raise PokemonAPIException(f"Failed to retrieve move data: {str(e)}")

    @staticmethod
    def _extract_stats(data: dict) -> Dict[str, int]:
        """Extract stats from Pokemon data."""
        return {
            stat['stat']['name']: stat['base_stat']
            for stat in get(data, 'stats', [])
        }

    @staticmethod
    def transform_pokemon_data(data: PokemonData) -> Pokemon:
        """Transform PokemonData to Pokemon format for battles."""
        return Pokemon(
            id=data.id,
            name=data.name,
            hp=get(data.stats, 'hp'),
            attack=get(data.stats, 'attack'),
            defense=get(data.stats, 'defense'),
            special_attack=get(data.stats, 'special-attack'),
            special_defense=get(data.stats, 'special-defense'),
            speed=get(data.stats, 'speed'),
            types=data.types,
            moves=data.moves[:4]  # Select first 4 moves
        )