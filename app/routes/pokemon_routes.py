# app/routes/pokemon_routes.py
from flask import Blueprint, jsonify
from app.exceptions import PokemonNotFoundException
from app.services.pokemon_service import PokemonService

def create_pokemon_blueprint(pokemon_service: PokemonService) -> Blueprint:
    pokemon_bp = Blueprint('pokemon', __name__)

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
        responses:
          404:
            description: Pokémon not found
        """
        try:
            pokemon_info = pokemon_service.get_pokemon_information(name)
            return jsonify(pokemon_info), 200
        except PokemonNotFoundException as e:
            return jsonify({'error': f'Pokemon {e.pokemon_name} not found'}), 404

    return pokemon_bp