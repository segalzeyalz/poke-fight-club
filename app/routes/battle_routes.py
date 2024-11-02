from flask import request, jsonify

from app.battle_logic import BattleSimulation
from app.battle_logic.move_handler import MoveHandler
from app.battle_logic.type_effectiveness import TypeEffectiveness
from app.cache.pokemon_cache import PokemonCacheManager
from app.routes import battle_bp
from app.services.battle_service import BattleService
from app.models import BattleRequest
from app.services.pokeapi_service import PokeAPIService


@battle_bp.route('/battles', methods=['POST'])
def create_battle():
    """
    Start a Pokémon battle between two specified Pokémon.
    ---
    tags:
      - Battles
    parameters:
      - name: pokemon1_name
        in: formData
        type: string
        required: true
        description: Name of the first Pokémon
      - name: pokemon2_name
        in: formData
        type: string
        required: true
        description: Name of the second Pokémon
    responses:
      200:
        description: Battle result with winner and battle log
        schema:
          type: object
          properties:
            winner:
              type: string
              description: Name of the winning Pokémon
            battle_log:
              type: array
              items:
                type: string
              description: Battle events log
      404:
        description: Pokémon not found
      500:
        description: Internal server error
    """
    battle_request = BattleRequest(**request.json)
    cache_manager = PokemonCacheManager()
    pokemon_api_service = PokeAPIService(base_url='https://pokeapi.co/api/v2/', cache_manager=cache_manager)
    type_effectiveness_service = TypeEffectiveness()
    pokemon_move_handler = MoveHandler(pokemon_api_service)
    battle_simulation = BattleSimulation(type_effectiveness_service=type_effectiveness_service,
                                         move_handler=pokemon_move_handler)

    battle_service = BattleService(pokeapi_service=pokemon_api_service, battle_simulation=battle_simulation)

    battle_result = battle_service.create_battle(battle_request.pokemon1, battle_request.pokemon2)
    return jsonify(battle_result.dict()), 201