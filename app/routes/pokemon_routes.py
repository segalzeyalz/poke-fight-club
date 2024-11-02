from flask import jsonify

from app.cache.pokemon_cache import PokemonCacheManager
from app.repositories.pokemon_repository import PokemonRepository
from app.routes import pokemon_bp
from app.services.pokeapi_service import PokeAPIService


@pokemon_bp.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    pokemon_repository = PokemonRepository()

    # Try to get Pokemon from database
    pokemon_info = pokemon_repository.get_pokemon_by_name(name)

    if not pokemon_info:
        # If not in database, fetch from PokeAPI
        pokemon_api_service = PokeAPIService(
            base_url='https://pokeapi.co/api/v2/',
            cache_manager=PokemonCacheManager()
        )
        api_pokemon_info = pokemon_api_service.get_pokemon_data(name)

        # Store in database
        pokemon_info = pokemon_repository.create_pokemon(
            name=api_pokemon_info.name,
            types=api_pokemon_info.types,
            stats=api_pokemon_info.stats
        )

    return jsonify(pokemon_info.serialize()), 200