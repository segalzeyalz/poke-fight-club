# app/repositories/pokemon_repository.py
from typing import List, Dict, Optional
import sqlalchemy as sa
from app.database import db
from app.database.models import Pokemon
from app.models import PokemonInfo


class PokemonRepository:
    def get_pokemon_by_name(self, name: str) -> Optional[PokemonInfo]:
        """
        Retrieve a Pokemon by name from the database.
        If not found, returns None.
        """
        pokemon = db.session.scalar(
            sa.select(Pokemon).where(sa.func.lower(Pokemon.name) == name.lower())
        )

        if pokemon:
            return PokemonInfo.from_db_model(pokemon)
        return None

    def create_pokemon(self, name: str, types: List[str], stats: Dict[str, int]) -> PokemonInfo:
        """
        Create a new Pokemon in the database.
        """
        # Ensure we have at least one type and at most two types
        if not types:
            raise ValueError("Pokemon must have at least one type")
        if len(types) > 2:
            raise ValueError("Pokemon cannot have more than two types")

        # Create new Pokemon instance
        pokemon = Pokemon(
            name=name.lower(),
            hp=stats.get('hp', 0),
            attack=stats.get('attack', 0),
            defense=stats.get('defense', 0),
            special_attack=stats.get('special-attack', 0),
            special_defense=stats.get('special-defense', 0),
            speed=stats.get('speed', 0),
            type1=types[0],
            type2=types[1] if len(types) > 1 else None
        )

        db.session.add(pokemon)
        db.session.commit()

        return PokemonInfo.from_db_model(pokemon)

    def update_pokemon(self, name: str, types: List[str], stats: Dict[str, int]) -> PokemonInfo:
        """
        Update an existing Pokemon in the database.
        If the Pokemon doesn't exist, creates it.
        """
        pokemon = db.session.scalar(
            sa.select(Pokemon).where(sa.func.lower(Pokemon.name) == name.lower())
        )

        if pokemon:
            pokemon.hp = stats.get('hp', 0)
            pokemon.attack = stats.get('attack', 0)
            pokemon.defense = stats.get('defense', 0)
            pokemon.special_attack = stats.get('special-attack', 0)
            pokemon.special_defense = stats.get('special-defense', 0)
            pokemon.speed = stats.get('speed', 0)
            pokemon.type1 = types[0]
            pokemon.type2 = types[1] if len(types) > 1 else None

            db.session.commit()
            return PokemonInfo.from_db_model(pokemon)
        return self.create_pokemon(name, types, stats)