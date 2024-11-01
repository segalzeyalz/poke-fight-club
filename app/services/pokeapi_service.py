import requests
from pydantic import ValidationError
from app.cache.cache import CacheManager
from app.models import PokemonData, Pokemon


class PokeAPIService:
    def __init__(self, base_url: str, cache_manager: CacheManager):
        self.base_url = base_url
        self.cache_manager = cache_manager

    def get_pokemon_data(self, pokemon_name: str) -> PokemonData:
        cached_data = self.cache_manager.get_pokemon_data(pokemon_name)
        if cached_data:
            return cached_data

        # If not cached, retrieve from API
        url = f'{self.base_url}/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
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
            except ValidationError as e:
                raise ValueError("Invalid data format") from e
        else:
            raise ValueError(f"Failed to retrieve data for {pokemon_name}")

    def get_move_data(self, move_name: str) -> dict:
        cached_move = self.cache_manager.get_pokemon_data(move_name)
        if cached_move:
            return cached_move

        url = f'{self.base_url}/move/{move_name}'
        response = requests.get(url)
        if response.status_code == 200:
            move_data = response.json()
            self.cache_manager.set_pokemon_data(move_name, move_data)  # Cache the move data
            return move_data
        else:
            raise ValueError(f"Failed to retrieve data for {move_name}")

    def transform_pokemon_data(self, data: PokemonData) -> Pokemon:
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
            moves=data.moves[:4]  # Select the first 4 moves or customize as needed
        )
