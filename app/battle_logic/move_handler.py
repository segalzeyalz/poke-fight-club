from typing import Dict

from app.models import Pokemon

class MoveHandler:
    def __init__(self, pokeapi_service: "PokeAPIService"):
        self.pokeapi_service = pokeapi_service

    def get_move_data(self, move_name: str) -> Dict:
        return self.pokeapi_service.get_move_data(move_name)

    @staticmethod
    def select_move(pokemon: Pokemon) -> str:
        first_move = pokemon.moves[0] if pokemon.moves else None
        return first_move
