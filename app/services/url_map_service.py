from typing import Dict
import requests
from app.config import Config
from app.exceptions import PokemonAPIException, PokemonNotFoundException


class PokemonURLMapper:
    def __init__(self, cache_manager):
        self.base_url = Config.POKEAPI_BASE_URL
        self.cache_manager = cache_manager
        self.pokemon_urls: Dict[str, str] = {}
        self._initialize_mapping()

    def _initialize_mapping(self) -> None:
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

    def get_pokemon_url(self, pokemon_name: str) -> str:
        pokemon_name = pokemon_name.lower()
        if pokemon_name not in self.pokemon_urls:
            raise PokemonNotFoundException(pokemon_name)
        return self.pokemon_urls[pokemon_name]

    @staticmethod
    def _make_api_request(url: str) -> requests.Response:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.Timeout:
            raise PokemonAPIException("Request timed out")
        except requests.RequestException as e:
            raise PokemonAPIException(f"API request failed: {str(e)}")