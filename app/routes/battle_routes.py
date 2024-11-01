from flask import request, jsonify

from app.battle_logic import BattleSimulation
from app.battle_logic.move_handler import MoveHandler
from app.battle_logic.type_effectiveness import TypeEffectiveness
from app.cache.cache import CacheManager
from app.routes import battle_bp
from app.services.battle_service import BattleService
from app.models import BattleRequest
from app.services.pokeapi_service import PokeAPIService


@battle_bp.route('/battles', methods=['POST'])
def create_battle():
    battle_request = BattleRequest(**request.json)
    cache_manager = CacheManager()
    pokemon_api_service = PokeAPIService(base_url='https://pokeapi.co/api/v2/pokemon', cache_manager=cache_manager)
    type_effectiveness_service = TypeEffectiveness()
    pokemon_move_handler = MoveHandler(pokemon_api_service)
    battle_simulation = BattleSimulation(type_effectiveness_service=type_effectiveness_service,
                                         move_handler=pokemon_move_handler)

    battle_service = BattleService(pokeapi_service=pokemon_api_service, battle_simulation=battle_simulation)

    battle_result = battle_service.create_battle(battle_request.pokemon1, battle_request.pokemon2)
    return jsonify(battle_result.dict()), 201