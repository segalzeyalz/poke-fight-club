class PokemonCacheManager:
    _instance = None
    _cache = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PokemonCacheManager, cls).__new__(cls)
        return cls._instance

    def get_pokemon_data(self, pokemon_name: str):
        pokemon_name = pokemon_name.lower()
        return self._cache.get(f'pokemon_{pokemon_name}')

    def set_pokemon_data(self, pokemon_name: str, data: dict):
        pokemon_name = pokemon_name.lower()
        self._cache[f'pokemon_{pokemon_name}'] = data

    def get_move_data(self, move_name: str) -> dict:
        move_name = move_name.lower()
        return self._cache.get(f'move_{move_name}')

    def set_move_data(self, move_name: str, data: dict):
        move_name = move_name.lower()
        self._cache[f'move_{move_name}'] = data
