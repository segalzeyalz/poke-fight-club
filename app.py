from flask import Flask
from flasgger import Swagger
from gunicorn.app.base import BaseApplication
from app.routes.battle_routes import create_battle_blueprint
from app.routes.pokemon_routes import pokemon_bp
from app.config import Config
from app.database import db
from app.cache.pokemon_cache import PokemonCacheManager
from app.services.pokeapi_service import PokeAPIService
from app.battle_logic.battle_simulation import BattleSimulation
from app.battle_logic.move_handler import MoveHandler
from app.battle_logic.type_effectiveness import TypeEffectiveness
from app.services.battle_service import BattleService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cache_manager = PokemonCacheManager()
    pokemon_api_service = PokeAPIService(base_url='https://pokeapi.co/api/v2/', cache_manager=cache_manager)
    type_effectiveness_service = TypeEffectiveness()
    move_handler = MoveHandler(pokemon_api_service)
    battle_simulation = BattleSimulation(type_effectiveness_service=type_effectiveness_service,
                                         move_handler=move_handler)
    battle_service = BattleService(pokeapi_service=pokemon_api_service, battle_simulation=battle_simulation)

    app.register_blueprint(create_battle_blueprint(battle_service), url_prefix="/api")
    app.register_blueprint(pokemon_bp, url_prefix="/api")

    db.init_app(app)
    Swagger(app)

    with app.app_context():
        db.create_all()

    return app

class GunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    app = create_app()

    options = {
        "bind": "0.0.0.0:5001",
        "workers": 4,
    }

    GunicornApp(app, options).run()
