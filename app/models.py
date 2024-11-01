from typing import List, Dict

from pydantic import BaseModel

class PokemonInfo(BaseModel):
    name: str
    types: List[str]
    stats: Dict[str, int]

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