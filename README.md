# Pokémon Battle Simulation API

This project is a Pokémon Battle Simulation API that enables turn-based battles between Pokémon. It integrates with [PokeAPI](https://pokeapi.co/) for data enrichment and includes containerization for easy deployment.

## Features
- **Battle Simulation**: Turn-based battles using Pokémon stats (HP, Attack, Defense)
- **External API Integration**: Real-time data from PokeAPI
- **Data Persistence**: Battle history storage
- **Caching**: Optimized API performance
- **Error Handling**: Comprehensive error management
- **Testing**: Unit and integration test coverage

## Quick Start

### Installation
1. Clone the repository:
```bash
git clone https://github.com/segalzeyalz/poke-fight-club.git
cd poke-fight-club
```

2. Build and start containers:
```bash
docker-compose up --build
```

3. Access the API:
```plaintext
API: http://localhost:5001
Swagger UI: http://localhost:5001/apidocs
```

### API Access Points
All API endpoints are accessible through port 5001. For example:
- API Base URL: `http://localhost:5001`
- Swagger Documentation: `http://localhost:5001/apidocs`
- Battle Endpoint: `http://localhost:5001/battle`
- Pokemon Information: `http://localhost:5001/pokemon/{name}`


## Project Structure

### Key Directories
```plaintext
app/
├── battle_logic/          # Battle simulation core
├── database/             # Data models and schema
├── repositories/         # Data access layer
├── services/            # Business logic
├── routes/              # API endpoints
└── tests/              # Test suites
```

### Component Details
- **`battle_logic/`**: 
  - Turn-based battle system
  - Type effectiveness calculations
  - Move damage computations

- **`database/`**: 
  - SQLite database (development)
  - Models for Pokémon and battles
  - Migration scripts

- **`repositories/`**: 
  - Pokémon data management
  - Battle record storage
  - Data access patterns

- **`services/`**: 
  - PokeAPI integration
  - Battle orchestration
  - Data transformation


### Current Architecture Trade-offs

1. **Database Choice (SQLite)**
   - **Current Implementation**: Using SQLite for simplicity and development speed
   - **Production Improvement**: 
     - Implement PostgreSQL with docker-compose
     - Offers robust transaction support and concurrent access
     - Better suited for containerized environments
     - Supports connection pooling for better resource management

2. **Repository Pattern Implementation**
   - **Current Implementation**: PokemonRepository handling multiple responsibilities
   - **Production Improvement**: 
     - Implement Factory Pattern with specialized classes:
       ```python
       class PokemonReader:
           def get_by_name(self, name: str): pass
       
       class PokemonWriter:
           def create(self, data: Dict): pass
       
       class PokemonUpdater:
           def update(self, name: str, data: Dict): pass
       ```

3. **PokeAPI Service Structure**
   - **Current Implementation**: Single service handling API calls, caching, and transformations
   - **Production Improvement**: 
     - Split into dedicated services:
     ```python
     class PokemonDataFetcher:
         def fetch_pokemon(self): pass
     
     class PokemonDataTransformer:
         def transform(self): pass
     
     class PokemonCacheManager:
         def manage_cache(self): pass
     ```

4. **Request Processing**
   - **Current Implementation**: Synchronous request processing
   - **Production Improvement**: 
     - Implement AWS SQS for battle requests:
       - Asynchronous processing
       - Better load handling
       - Automatic retry mechanism
     ```python
     class BattleQueue:
         def __init__(self):
             self.sqs = boto3.client('sqs')
             
         def enqueue_battle(self, battle_data):
             return self.sqs.send_message(
                 QueueUrl=QUEUE_URL,
                 MessageBody=json.dumps(battle_data)
             )
     ```

5. **Load Distribution**
   - **Current Implementation**: Single container deployment
   - **Production Improvement**: 
     - Kubernetes deployment with:
       - Horizontal Pod Autoscaling
       - Load balancing
       - Health checks
       - Rolling updates
     ```yaml
     apiVersion: autoscaling/v2
     kind: HorizontalPodAutoscaler
     metadata:
       name: pokemon-battle-api
     spec:
       scaleTargetRef:
         apiVersion: apps/v1
         kind: Deployment
         name: pokemon-battle-api
       minReplicas: 2
       maxReplicas: 10
     ```

6. **Caching Strategy**
   - **Current Implementation**: Basic in-memory caching
   - **Production Improvement**: 
     - Implement Python cachetools with TTL:
       - Thread-safe operations
       - Automatic cache invalidation
       - Memory usage control
     ```python
     from cachetools import TTLCache
     
     cache = TTLCache(maxsize=100, ttl=3600)
     ```