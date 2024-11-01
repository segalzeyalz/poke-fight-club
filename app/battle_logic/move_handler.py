import requests

class MoveHandler:
    @staticmethod
    def get_move_data(move_name: str) -> dict:
        url = f'https://pokeapi.co/api/v2/move/{move_name}'
        response = requests.get(url)
        return response.json()

    @staticmethod
    def select_move(pokemon: dict) -> dict:
        # Select a move for a Pokémon based on battle conditions
        pass