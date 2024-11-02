import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.json")

with open(config_path) as config_file:
    config_data = json.load(config_file)

class Config:
    POKEAPI_BASE_URL = os.getenv("POKEAPI_BASE_URL", config_data["POKEAPI_BASE_URL"])
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", config_data["DATABASE_URL"])
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
