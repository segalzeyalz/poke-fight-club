import os
import json

with open("app/config/config.json") as config_file:
    config_data = json.load(config_file)

class Config:
    POKEAPI_BASE_URL = os.getenv("POKEAPI_BASE_URL", config_data["POKEAPI_BASE_URL"])
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", config_data["DATABASE_URL"])  # Correct variable name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
