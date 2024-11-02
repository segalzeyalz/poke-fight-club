from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, Field

class PokemonType(str, Enum):
    NORMAL = "normal"
    FIRE = "fire"
    WATER = "water"
    ELECTRIC = "electric"
    GRASS = "grass"
    ICE = "ice"
    FIGHTING = "fighting"
    POISON = "poison"
    GROUND = "ground"
    FLYING = "flying"
    PSYCHIC = "psychic"
    BUG = "bug"
    ROCK = "rock"
    GHOST = "ghost"
    DARK = "dark"
    DRAGON = "dragon"
    STEEL = "steel"
    FAIRY = "fairy"

class Stats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int = Field(alias="special-attack")
    special_defense: int = Field(alias="special-defense")
    speed: int

class PokemonInfo(BaseModel):
    id: int
    name: str
    types: List[PokemonType]
    stats: Stats

    @classmethod
    def from_db_model(cls, pokemon_db: 'Pokemon') -> 'PokemonInfo':
        types = [pokemon_db.type1]
        if pokemon_db.type2:
            types.append(pokemon_db.type2)

        stats = {
            'hp': pokemon_db.hp,
            'attack': pokemon_db.attack,
            'defense': pokemon_db.defense,
            'special-attack': pokemon_db.special_attack,
            'special-defense': pokemon_db.special_defense,
            'speed': pokemon_db.speed
        }

        return cls(
            id=pokemon_db.id,
            name=pokemon_db.name,
            types=types,
            stats=stats
        )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'types': self.types,
            'stats': self.stats.dict()
        }

class BattleRequest(BaseModel):
    pokemon1: str
    pokemon2: str

class BattleResult(BaseModel):
    winner: str
    battle_log: List[str]


class Pokemon(BaseModel):
    id: int
    name: str
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    types: List[str]
    moves: List[str]

    class Config:
        arbitrary_types_allowed = True

class PokemonData(BaseModel):
    id: int
    name: str
    stats: dict
    types: list
    moves: list