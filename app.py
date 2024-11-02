from flask import Flask
from flasgger import Swagger

from app.routes.battle_routes import battle_bp
from app.routes.pokemon_routes import pokemon_bp  # Add this import
from app.config import Config
from app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(battle_bp, url_prefix="/api")
    app.register_blueprint(pokemon_bp, url_prefix="/api")

    db.init_app(app)
    # Initialize Swagger - API documentation
    Swagger(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5001)