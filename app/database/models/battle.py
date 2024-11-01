from app.database import db

class BattleModel(db.Model):
    __tablename__ = "battles"
    id = db.Column(db.Integer, primary_key=True)
    pokemon1_id = db.Column(db.Integer)
    pokemon2_id = db.Column(db.Integer)
    winner = db.Column(db.String)
    battle_log = db.Column(db.Text)

    def __init__(self, pokemon1_id: int, pokemon2_id: int, winner, battle_log):
        self.pokemon1_id = pokemon1_id
        self.pokemon2_id = pokemon2_id
        self.winner = winner
        self.battle_log = battle_log
