from typing import List

from app.database import db
from sqlalchemy import Column, Integer, String, Text

class Battle(db.Model):
    __tablename__ = 'battles'

    id = Column(Integer, primary_key=True)
    pokemon1_id = Column(Integer, nullable=False)
    pokemon2_id = Column(Integer, nullable=False)
    winner = Column(String(50), nullable=False)
    battle_log = Column(Text, nullable=False)

    def set_battle_log(self, log_list: List[str]):
        """Convert list of log entries to string"""
        self.battle_log = '\n'.join(log_list)

    def get_battle_log(self) -> List[str]:
        """Convert stored string back to list"""
        return self.battle_log.split('\n') if self.battle_log else []