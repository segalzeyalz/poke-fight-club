import requests

class PokeAPIService:
    @staticmethod
    def get_pokemon_data(pokemon_name: str) -> dict:
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        return response.json()