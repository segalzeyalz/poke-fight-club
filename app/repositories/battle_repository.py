from typing import List

from app.database import db
from app.database.models import Battle


class BattleRepository:
    @staticmethod
    def create_battle(pokemon1_id: int, pokemon2_id: int, winner: str, battle_log: List[str]):
        battle = Battle(pokemon1_id=pokemon1_id, pokemon2_id=pokemon2_id, winner=winner)
        battle.set_battle_log(battle_log)
        db.session.add(battle)
        db.session.commit()
