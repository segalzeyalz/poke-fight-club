class BattleRepository:
    @staticmethod
    def create_battle(pokemon1_id: int, pokemon2_id: int, winner: str, battle_log: List[str]):
        battle = BattleModel(pokemon1_id=pokemon1_id, pokemon2_id=pokemon2_id, winner=winner, battle_log=battle_log)
        db.session.add(battle)
        db.session.commit()

    @staticmethod
    def get_battle_by_id(battle_id: int) -> BattleModel:
        return BattleModel.query.get(battle_id)