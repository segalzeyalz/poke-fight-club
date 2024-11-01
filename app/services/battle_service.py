from app.battle_logic.move_handler import MoveHandler
from app.battle_logic.type_effectiveness import TypeEffectiveness
from app.cache.cache import CacheManager
from app.services.pokeapi_service import PokeAPIService
from app.battle_logic.battle_simulation import BattleSimulation
from app.database.models.battle import BattleModel
from app.database import db
from app.models import BattleResult

class BattleService:
    def __init__(self, pokeapi_service: PokeAPIService, battle_simulation: BattleSimulation):
        self.pokeapi_service = pokeapi_service
        self.battle_simulation = battle_simulation

    def create_battle(self, pokemon1_name: str, pokemon2_name: str) -> BattleResult:
        # Retrieve or cache Pokémon data
        pokemon1_data = self.pokeapi_service.get_pokemon_data(pokemon1_name)
        pokemon2_data = self.pokeapi_service.get_pokemon_data(pokemon2_name)

        # Transform to Pokemon objects for battle
        pokemon1 = self.pokeapi_service.transform_pokemon_data(pokemon1_data)
        pokemon2 = self.pokeapi_service.transform_pokemon_data(pokemon2_data)

        battle_sim = self.battle_simulation
        winner, battle_log = battle_sim.simulate_battle(pokemon1, pokemon2)

        # Store battle result in the database
        battle_result = BattleModel(
            pokemon1_id=pokemon1.id,
            pokemon2_id=pokemon2.id,
            winner=winner,
            battle_log=battle_log
        )
        db.session.add(battle_result)
        db.session.commit()

        return BattleResult(winner=winner, battle_log=log)
