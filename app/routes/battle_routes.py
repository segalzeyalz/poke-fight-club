from flask import request, jsonify
from app.routes import battle_bp
from app.services.battle_service import BattleService
from app.models import BattleRequest

@battle_bp.route('/battles', methods=['POST'])
def create_battle():
    battle_request = BattleRequest(**request.json)
    battle_result = BattleService.create_battle(battle_request.pokemon1, battle_request.pokemon2)
    return jsonify(battle_result.dict())