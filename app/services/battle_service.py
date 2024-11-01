from app.database import db
from app.models import BattleResult


class BattleService:
    @staticmethod
    def create_battle(pokemon1_name: str, pokemon2_name: str) -> BattleResult:
        # Get Pokémon info from the PokéAPI
        pokemon1_info = PokeAPI.get_pokemon_info(pokemon1_name)
        pokemon2_info = PokeAPI.get_pokemon_info(pokemon2_name)

        # Create Pokémon objects
        pokemon1 = Pokemon(pokemon1_info)
        pokemon2 = Pokemon(pokemon2_info)

        # Simulate the battle
        battle = Battle(pokemon1, pokemon2)
        winner, battle_log = battle.simulate_battle()

        # Save the battle to the database
        battle_model = BattleModel(pokemon1_id=pokemon1_info['id'], pokemon2_id=pokemon2_info['id'], winner=winner, battle_log=battle_log)
        db.session.add(battle_model)
        db.session.commit()

        return BattleResult(winner=winner.name, battle_log=battle_log)