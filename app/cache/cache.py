class CacheManager:
    _instance = None
    _cache = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CacheManager, cls).__new__(cls)
        return cls._instance

    def get_pokemon_data(self, pokemon_name: str):
        return self._cache.get(pokemon_name)

    def set_pokemon_data(self, name: str, data: dict):
        self._cache[name] = data
