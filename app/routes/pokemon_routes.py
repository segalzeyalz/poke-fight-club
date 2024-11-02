from flask import jsonify

from app.cache.pokemon_cache import PokemonCacheManager
from app.routes import pokemon_bp
from app.services.pokeapi_service import PokeAPIService


@pokemon_bp.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    pokemon_api_service = PokeAPIService(base_url='https://pokeapi.co/api/v2/',
                                         cache_manager=PokemonCacheManager())
    pokemon_info = pokemon_api_service.get_pokemon_data(name)
    return jsonify(pokemon_info.dict()), 200