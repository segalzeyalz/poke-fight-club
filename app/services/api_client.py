import requests
from app.exceptions import PokemonAPIException, PokemonNotFoundException


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str) -> dict:
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise PokemonAPIException("Request timed out")
        except requests.RequestException as e:
            if 'pokemon' in endpoint and response.status_code == 404:
                raise PokemonNotFoundException(f"Failed to get Pokemon data: {str(e)}")
            raise PokemonAPIException(f"API request failed: {str(e)}")