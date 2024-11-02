from flask import jsonify

from app.cache.pokemon_cache import PokemonCacheManager
from app.repositories.pokemon_repository import PokemonRepository
from app.routes import pokemon_bp
from app.services.pokeapi_service import PokeAPIService


@pokemon_bp.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    """
    Retrieve information for a specified Pokémon.
    ---
    tags:
      - Pokémon
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Name of the Pokémon
    responses:
      200:
        description: Pokémon data
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Pokémon ID
            name:
              type: string
              description: Pokémon name
            hp:
              type: integer
              description: Hit points of the Pokémon
            attack:
              type: integer
              description: Attack stat
            defense:
              type: integer
              description: Defense stat
            special_attack:
              type: integer
              description: Special attack stat
            special_defense:
              type: integer
              description: Special defense stat
            speed:
              type: integer
              description: Speed stat
            types:
              type: array
              items:
                type: string
              description: List of Pokémon types
      404:
        description: Pokémon not found
      500:
        description: Internal server error
    """
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