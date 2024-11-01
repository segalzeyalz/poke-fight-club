# Pokémon Battle Simulation API

This project is a Pokémon Battle Simulation API designed to pit two Pokémon against each other in a turn-based battle. It uses data from the [PokeAPI](https://pokeapi.co/) to fetch Pokémon details, simulates battles based on Pokémon attributes, and saves battle data in a database. The project is designed with modularity and containerization in mind, using Docker for easy deployment.

## Features
- **Battle Simulation**: Simulates turn-by-turn Pokémon battles based on stats such as HP, Attack, Defense, and more.
- **External API Integration**: Fetches Pokémon data from PokeAPI to enrich battle simulations.
- **Data Persistence**: Saves battle history in a database.
- **Caching**: Caches Pokémon data to reduce API calls and improve performance.
- **Error Handling**: Provides robust error handling for various scenarios.
- **Testing**: Includes unit tests for critical components.


### Key Directories
- **`battle_logic`**: Contains the core battle simulation logic, including handling moves and type effectiveness.
- **`database`**: Sets up the database schema and models, storing Pokémon and battle data.
- **`repositories`**: Manages data access, with `pokemon_repository.py` for Pokémon data and `battle_repository.py` for battle records.
- **`services`**: Implements business logic, calling external APIs and coordinating battle sequences.
- **`routes`**: Defines the API endpoints for battle initiation and Pokémon information retrieval.
- **`tests`**: Contains unit tests for the API, battle logic, repositories, and routes.

### Running the API Instructions
Build the Docker Container: Ensure Docker is installed and running.

```bash
docker-compose build
``` 
Accessing the API: Once the container is up, the API should be accessible at http://localhost:8000.

### API Endpoints
- **POST `/battle`:** Initiates a battle between two Pokémon. Request body:
```json
{
    "pokemon1": "charmander",
    "pokemon2": "squirtle"
}
```
Response:
```json
{
    "winner": "charmander",
    "log": [
        "charmander used Ember! It's super effective! Squirtle fainted.",
        "charmander wins!"
    ]
}
```

.... TO CONTINUE...