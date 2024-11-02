from typing import Dict
from pydash import get
from app.models import PokemonData, Pokemon

class PokemonDataTransformer:
    @staticmethod
    def transform_to_pokemon_data(raw_data: dict) -> PokemonData:
        types = list(map(lambda t: t['type']['name'], raw_data.get('types', [])))
        moves = list(map(lambda m: m['move']['name'], raw_data.get('moves', [])))

        return PokemonData(
            id=get(raw_data, 'id'),
            name=get(raw_data, 'name'),
            stats=PokemonDataTransformer._extract_stats(raw_data),
            types=types,
            moves=moves[:4]
        )

    @staticmethod
    def transform_to_pokemon(data: PokemonData) -> Pokemon:
        return Pokemon(
            id=data.id,
            name=data.name,
            hp=get(data.stats, 'hp'),
            attack=get(data.stats, 'attack'),
            defense=get(data.stats, 'defense'),
            special_attack=get(data.stats, 'special-attack'),
            special_defense=get(data.stats, 'special-defense'),
            speed=get(data.stats, 'speed'),
            types=data.types,
            moves=data.moves[:4]
        )

    @staticmethod
    def _extract_stats(data: dict) -> Dict[str, int]:
        return {
            stat['stat']['name']: stat['base_stat']
            for stat in get(data, 'stats', [])
        }