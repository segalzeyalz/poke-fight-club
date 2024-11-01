from flask import jsonify

from app.cache.cache import CacheManager
from app.routes import pokemon_bp
from app.services.pokeapi_service import PokeAPIService


@pokemon_bp.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    pokemon_api_service = PokeAPIService(base_url='https://pokeapi.co/api/v2/pokemon',
                                         cache_manager=CacheManager())
    pokemon_info = pokemon_api_service.get_pokemon_data(name)
    return jsonify(pokemon_info.dict()), 200