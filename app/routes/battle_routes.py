from flask import Blueprint, request, jsonify
from app.models import BattleRequest
from app.services.pokeapi_service import POKEMON_NOT_FOUND


def create_battle_blueprint(battle_service):
    battle_bp = Blueprint('battle', __name__)

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
        battle_result = battle_service.create_battle(battle_request.pokemon1, battle_request.pokemon2)
        if battle_result == POKEMON_NOT_FOUND:
            return jsonify({'message': 'One or more Pokémon not found'}), 404
        return jsonify(battle_result.dict()), 201

    return battle_bp
