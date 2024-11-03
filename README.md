# Pokémon Battle Simulation API

This project is a Pokémon Battle Simulation API that enables turn-based battles between Pokémon. It integrates with [PokeAPI](https://pokeapi.co/) for data enrichment and includes containerization for easy deployment.

## Features
- **Battle Simulation**: Turn-based battles using Pokémon stats (HP, Attack, Defense)
- **External API Integration**: Real-time data from PokeAPI
- **Data Persistence**: Battle history storage
- **Caching**: Optimized API performance
- **Error Handling**: Comprehensive error management using Pydentic
- **Testing**: Unit test coverage

## Quick Start

### Installation
1. Clone the repository:
```bash
git clone https://github.com/segalzeyalz/poke-fight-club.git
cd poke-fight-club
```

2. Build and start containers:
```bash
docker build -t flask-app .
docker run -p 5001:5001 flask-app
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

3. **Request Processing**
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

4. **Load Distribution**
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

5. **Caching Strategy**
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

6. **Security Enhancements**
   1. API Rate Limiting 
       - **Current Implementation**: None
       - **Production Improvement**: 
         - rate-limiting middleware like flask-limiter to limit requests per user or IP
    2. Authentication & Authorization
       - **Current Implementation**: None
       - **Production Improvement**:  Implement JWT to validate requests, using Flask-JWT.

7. **Enhanced Observability**
   1. **Logging and Monitoring**
      - **Current Implementation**: Basic logging
      - **Production Improvement**:
        - Implement structured logging  in JSON format for compatibility with log aggregation tools.
        - Integrate splunk for logging services

   2. **Tracing**
      - **Current Implementation**: None
      - **Production Improvement**:
        - Use distributed tracing with **OpenTelemetry**.
        - This allows tracking each stage of a request and provides more in-depth diagnostics during debugging.

   3. **Metrics Collection**
      - **Current Implementation**: None
      - **Production Improvement**:
        - Integrate **Prometheus** with **Grafana** for tracking key metrics like request latencies, API response times, cache hit/miss ratios, and error rates.

8. **Developer Experience Improvements**
   1. **CI/CD Pipeline**
      - **Current Implementation**: None
      - **Production Improvement**:
        - Set up a CI/CD pipeline using **GitHub Actions** with testing + deployemnt after pull requests to master using argo-cd.
        - This pipeline would run unit and integration tests automatically on each pull request, and deploy changes to staging or production upon successful test completion.
   
   2. **Automated Testing and Test Coverage**
      - **Current Implementation**: Basic unit and integration testing
      - **Production Improvement**:
        - Extend test suite with load testing (e.g., using `locust` or `k6`) to ensure the API can handle expected traffic.
        - Integrate test coverage tracking to identify untested paths in the code and improve reliability for critical battle logic.

9. **Resilience and Disaster Recovery**
   1. **Database Backups and Recovery**
      - **Current Implementation**: None
      - **Production Improvement**:
        - Schedule automated PostgreSQL backups stored in **AWS S3** or another reliable storage service.
        - Implement periodic restoration tests to verify backup integrity and ensure quick recovery in case of data loss or corruption.
   
   2. **Graceful Degradation**
      - **Current Implementation**: None
      - **Production Improvement**:
        - Implement a fallback mechanism for external dependencies (e.g., PokeAPI). When external services are unavailable, serve cached data if available or queue requests for later processing.
        - Display a "Service Unavailable" message or a cached response to prevent service disruption during outages.

10. **Enhanced Deployment Flexibility**
   1. **Multi-Region Deployment for High Availability**
      - **Current Implementation**: Single-region deployment
      - **Production Improvement**:
        - Deploy across multiple regions with a global load balancer (e.g., **AWS Global Accelerator** or **Cloudflare Load Balancer**) to ensure high availability and reduced latency.
        - Configure automatic failover between regions for uninterrupted service during outages in one region.

   2. **Container Orchestration with Helm Charts**
      - **Current Implementation**: Basic Kubernetes configuration
      - **Production Improvement**:
        - Use **Helm** to package Kubernetes configurations into reusable charts, making it easier to configure, upgrade, and roll back deployments.
        - Helm simplifies multi-environment deployments by allowing parameterized configurations for development, staging, and production environments.

11. **Enhanced Data Model for Pokémon Moves**
      - **Current Implementation**: Pokémon moves stored as list in Pokémon model
      - **Production Improvement**:
        - Refactor database schema to store moves in a separate `moves` table with attributes such as `power`, `accuracy`, `type`, and `damage_class`.
        - This improves flexibility and makes querying and managing individual moves easier, especially if future requirements include move updates or expansions.
