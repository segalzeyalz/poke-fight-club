# app/services/pokeapi_service.py
from pydantic import ValidationError
from toolz import get

from app.models import PokemonData, Pokemon
from app.exceptions import (
    PokemonNotFoundException,
    PokemonAPIException,
    MoveNotFoundException,
    InvalidDataException
)
from app.services.data_tranformer import PokemonDataTransformer
from app.services.api_client import APIClient


class PokeAPIService:
    def __init__(self, cache_manager: 'PokemonCacheManager', url_mapper: 'PokemonURLMapper' = None,
                 api_client: 'APIClient' = None, data_transformer: 'PokemonDataTransformer' = None):
        self.cache_manager = cache_manager
        self.url_mapper = url_mapper
        self.api_client = api_client
        self.data_transformer = data_transformer

    def get_pokemon_data(self, pokemon_name: str) -> PokemonData:
        cached_data = self.cache_manager.get_pokemon_data(pokemon_name)
        if cached_data:
            return cached_data

        try:
            url = self.url_mapper.get_pokemon_url(pokemon_name)
        except PokemonNotFoundException:
            raise PokemonNotFoundException(pokemon_name)

        try:
            raw_data = self.api_client.get(f"pokemon/{pokemon_name}")
            pokemon_data = self.data_transformer.transform_to_pokemon_data(raw_data)

            self.cache_manager.set_pokemon_data(pokemon_name, pokemon_data)
            return pokemon_data

        except ValidationError as e:
            raise InvalidDataException(f"Invalid Pokemon data format: {str(e)}")

        except Exception as e:
            raise PokemonAPIException(f"Failed to get Pokemon data: {str(e)}")

    def get_move_data(self, move_name: str) -> dict:
        if not move_name:
            raise ValueError("Move name cannot be empty")

        cached_move = self.cache_manager.get_move_data(move_name)
        if cached_move:
            return cached_move

        try:
            move_data = self.api_client.get(f"move/{move_name}")
            simplified_move_data = {
                'name': move_data.get('name'),
                'power': move_data.get('power', 0),
                'type': get(['type', 'name'], move_data),
                'damage_class': get(['damage_class', 'name'], move_data)
            }

            self.cache_manager.set_move_data(move_name, simplified_move_data)
            return simplified_move_data

        except PokemonAPIException as e:
            if getattr(e, 'status_code', None) == 404:
                raise MoveNotFoundException(f"Move {move_name} not found")
            raise

    def transform_pokemon_data(self, data: PokemonData) -> Pokemon:
        return self.data_transformer.transform_to_pokemon(data)