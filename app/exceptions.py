from typing import Optional


class PokemonNotFoundException(Exception):
    def __init__(self, pokemon_name: str):
        self.pokemon_name = pokemon_name
        super().__init__(f"Pokemon '{pokemon_name}' not found in the database.")

    def __str__(self):
        return f"PokemonNotFoundException: '{self.pokemon_name}' was not found."

class PokemonAPIException(Exception):
    def __init__(self, message: str, url: Optional[str] = None, status_code: Optional[int] = None):
        self.url = url
        self.status_code = status_code
        super().__init__(message)

    def __str__(self):
        url_info = f"URL: {self.url}" if self.url else ""
        status_info = f"Status Code: {self.status_code}" if self.status_code else ""
        additional_info = f" ({url_info} {status_info})" if (url_info or status_info) else ""
        return f"PokemonAPIException: {self.args[0]}{additional_info}"

class MoveNotFoundException(Exception):
    def __init__(self, move_name: str):
        self.move_name = move_name
        super().__init__(f"Move '{move_name}' not found in the API.")

    def __str__(self):
        return f"MoveNotFoundException: '{self.move_name}' is unavailable or does not exist."

class InvalidDataException(Exception):
    def __init__(self, data_name: str, details: Optional[str] = None):
        self.data_name = data_name
        self.details = details
        super().__init__(f"Invalid data for '{data_name}'.")

    def __str__(self):
        details_info = f" Details: {self.details}" if self.details else ""
        return f"InvalidDataException: '{self.data_name}' has an invalid format.{details_info}"
