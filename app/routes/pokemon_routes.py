from flask import jsonify
from app.routes import pokemon_bp
from app.services.pokeapi_service import PokeAPIService

@pokemon_bp.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    pokemon_info = PokeAPIService.get_pokemon_data(name)
    return jsonify(pokemon_info.dict())