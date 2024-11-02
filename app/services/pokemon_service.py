from app.repositories.pokemon_repository import PokemonRepository
from app.services.pokeapi_service import PokeAPIService


class PokemonService:
    def __init__(self, pokemon_repository: PokemonRepository, pokeapi_service: PokeAPIService):
        self.pokemon_repository = pokemon_repository
        self.pokeapi_service = pokeapi_service

    def get_pokemon_information(self, name: str) -> dict:
        pokemon_info = self.pokemon_repository.get_pokemon_by_name(name)

        if not pokemon_info:
            api_pokemon_info = self.pokeapi_service.get_pokemon_data(name)

            pokemon_info = self.pokemon_repository.create_pokemon(
                name=api_pokemon_info.name,
                types=api_pokemon_info.types,
                stats=api_pokemon_info.stats
            )

        return pokemon_info.serialize()