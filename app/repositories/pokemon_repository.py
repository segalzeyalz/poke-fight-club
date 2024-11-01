from typing import List, Dict

from app.models import PokemonInfo


class PokemonRepository:
    def get_pokemon_by_name(self, name: str) -> PokemonInfo:
        pass

    def create_pokemon(self, name: str, types: List[str], stats: Dict[str, int]) -> PokemonInfo:
        pass