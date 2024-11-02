from app.repositories.battle_repository import BattleRepository
from app.services.pokeapi_service import PokeAPIService
from app.battle_logic.battle_simulation import BattleSimulation
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

        winner, battle_log = self.battle_simulation.simulate_battle(pokemon1, pokemon2)

        BattleRepository.create_battle(pokemon1.id, pokemon2.id, winner, battle_log)

        return BattleResult(winner=winner, battle_log=battle_log)
