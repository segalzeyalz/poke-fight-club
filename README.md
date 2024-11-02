# Pokémon Battle Simulation API

This project is a Pokémon Battle Simulation API designed to pit two Pokémon against each other in a turn-based battle. It uses data from the [PokeAPI](https://pokeapi.co/) to fetch Pokémon details, simulates battles based on Pokémon attributes, and saves battle data in a database. The project is designed with modularity and containerization in mind, using Docker for easy deployment.

## Features
- **Battle Simulation**: Simulates turn-by-turn Pokémon battles based on stats such as HP, Attack, Defense, and more.
- **External API Integration**: Fetches Pokémon data from PokeAPI to enrich battle simulations.
- **Data Persistence**: Saves battle history in a database.
- **Caching**: Caches Pokémon data to reduce API calls and improve performance.
- **Error Handling**: Provides robust error handling for various scenarios.
- **Testing**: Includes unit tests for critical components.

## API Documentation
Navigate to http://localhost:5000/apidocs to access the API documentation using Swagger UI. The documentation provides details on the available endpoints, request/response formats, and example usage.

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

## Trade-offs and Future Improvements
1. **Pokémon State Management During Battles**: Currently, Pokémon state is stored in memory during battles. For scalability, consider storing state in a database or cache. Moreover, this is not reflected in pokemon fetches too
The main reason is the will to make it finished with all the endpoint and with the right structure.
2. ** Scalability and Concurrency**: The project is designed for single-instance battle simulations. Concurrent battles might cause performance issues and database contention. Additionally, multiple instances of the same Pokemon in parallel battles are not supported.
** Proposed Solution**: Implement a queue system to manage battle requests and distribute them across multiple worker instances. Use a distributed cache for storing Pokémon data and battle states.
I would use SNS and PostgreSQL as PostgreSQL offers robust transactions and advanced data integrity features.
Amazon SNS queues battle requests, allowing the application to handle high volume without overwhelming resources.
3. **Error Handling and Logging**: The project currently has basic error handling and logging. For production use, implement more robust error handling, logging, and monitoring to track issues and performance.
** Proposed Solution**: Use a logging library like Loguru or Python's built-in logging module to log errors, warnings, and information. Implement exception handling middleware to catch and log errors in the API.
