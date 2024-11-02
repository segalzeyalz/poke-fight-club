from flask import Flask
from flasgger import Swagger
from gunicorn.app.base import BaseApplication
from app.routes.battle_routes import battle_bp
from app.routes.pokemon_routes import pokemon_bp
from app.config import Config
from app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(battle_bp, url_prefix="/api")
    app.register_blueprint(pokemon_bp, url_prefix="/api")

    db.init_app(app)
    Swagger(app)

    # Initialize database
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
