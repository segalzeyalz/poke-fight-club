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