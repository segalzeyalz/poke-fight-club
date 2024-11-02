from app.database import db
from sqlalchemy import Column, Integer, String, Text

class Battle(db.Model):
    __tablename__ = 'battles'

    id = Column(Integer, primary_key=True)
    pokemon1_id = Column(Integer, nullable=False)
    pokemon2_id = Column(Integer, nullable=False)
    winner = Column(String(50), nullable=False)
    log = Column(Text, nullable=False)
