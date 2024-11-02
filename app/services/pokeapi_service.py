import requests
from typing import Dict
from pydantic import ValidationError
from app.cache.pokemon_cache import PokemonCacheManager
from app.models import PokemonData, Pokemon


class PokeAPIService:
    def __init__(self, base_url: str, cache_manager: PokemonCacheManager):
        self.base_url = base_url
        self.cache_manager = cache_manager
        self.pokemon_urls: Dict[str, str] = {}
        self._initialize_pokemon_mapping()

    def _initialize_pokemon_mapping(self) -> None:
        """Initialize the mapping between Pokemon names and their URLs."""
        try:
            # First, check if the mapping is in cache
            cached_mapping = self.cache_manager.get_pokemon_data('pokemon_url_mapping')
            if cached_mapping:
                self.pokemon_urls = cached_mapping
                return

            # If not in cache, fetch from API
            url = f'{self.base_url}pokemon?offset=0&limit=1302'
            all_pokemon = []
            next_url = url

            # Fetch all pages
            while next_url:
                response = requests.get(next_url)
                if response.status_code != 200:
                    raise ValueError("Failed to initialize Pokemon mapping")

                data = response.json()
                all_pokemon.extend(data['results'])
                next_url = data['next']

            # Create the mapping
            self.pokemon_urls = {
                pokemon['name']: pokemon['url']
                for pokemon in all_pokemon
            }

            # Cache the mapping
            self.cache_manager.set_pokemon_data('pokemon_url_mapping', self.pokemon_urls)

        except Exception as e:
            raise ValueError(f"Failed to initialize Pokemon mapping: {str(e)}")

    def get_pokemon_url(self, pokemon_name: str) -> str:
        """Get the URL for a specific Pokemon."""
        pokemon_name = pokemon_name.lower()  # Normalize name to lowercase
        if pokemon_name not in self.pokemon_urls:
            raise ValueError(f"Pokemon {pokemon_name} not found")
        return self.pokemon_urls[pokemon_name]

    def get_pokemon_data(self, pokemon_name: str) -> PokemonData:
        pokemon_name = pokemon_name.lower()  # Normalize name to lowercase

        # Check cache first
        cached_data = self.cache_manager.get_pokemon_data(pokemon_name)
        if cached_data:
            return cached_data

        # If not cached, retrieve from API using the mapped URL
        try:
            url = self.get_pokemon_url(pokemon_name)
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                pokemon_data = PokemonData(
                    id=data['id'],
                    name=data['name'],
                    stats={stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
                    types=[t['type']['name'] for t in data['types']],
                    moves=[move['move']['name'] for move in data['moves']]
                )
                # Cache the data
                self.cache_manager.set_pokemon_data(pokemon_name, pokemon_data)
                return pokemon_data
            else:
                raise ValueError(f"Failed to retrieve data for {pokemon_name}")

        except ValidationError as e:
            raise ValueError("Invalid data format") from e

    def get_move_data(self, move_name: str) -> dict:
        """Get data for a specific move."""
        if not move_name:
            raise ValueError("Move name cannot be empty")

        move_name = move_name.lower()

        # Check cache first
        cached_move = self.cache_manager.get_move_data(move_name)
        if cached_move:
            return cached_move

        # Make API request
        url = f'{self.base_url}move/{move_name}'
        response = requests.get(url)

        if response.status_code == 200:
            move_data = response.json()
            # Extract only the data we need
            simplified_move_data = {
                'name': move_data['name'],
                'power': move_data.get('power', 0),
                'type': move_data['type']['name'],
                'damage_class': move_data['damage_class']['name']
            }
            # Cache the simplified data
            self.cache_manager.set_move_data(move_name, simplified_move_data)
            return simplified_move_data
        else:
            raise ValueError(f"Failed to retrieve data for move {move_name}")

    @staticmethod
    def transform_pokemon_data(data: PokemonData) -> Pokemon:
        """Transform PokemonData to Pokemon format for battles."""
        return Pokemon(
            id=data.id,
            name=data.name,
            hp=data.stats['hp'],
            attack=data.stats['attack'],
            defense=data.stats['defense'],
            special_attack=data.stats['special-attack'],
            special_defense=data.stats['special-defense'],
            speed=data.stats['speed'],
            types=data.types,
            moves=data.moves[:4]  # Select first 4 moves
        )