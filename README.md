# Gameloft Profile Matcher Service

## Overview

This project showcases a profile matching microservice designed to evaluate whether a given player profile qualifies for specific game campaigns. The service checks player data against campaign matcher rules and updates the profile with active campaigns accordingly. It s built with **FastAPI**, follows **Hexagonal Architecture**, and uses **Domain-Driven Design** principles to ensure separation of concerns and testability.

---

## Prerequisites

- Python 3.11+
- `pipenv` 

To install pipenv:
```bash
pip install pipenv
```

---

## System Design

### Architectural Layers

```
.
├── app/                      
│   ├── adapters/             # Infrastructure adapters (DB, APIs)
│   │   ├── campaign_api/     # Fake external campaign API
│   │   ├── db/               # SQLAlchemy models and persistence logic
│   │   ├── fast_api/         # FastAPI route handlers
│   │   └── dependencies.py   # Dependency injection setup
│   ├── domain/               # Domain logic and core models
│   │   ├── models/           # Pydantic domain models for Campaign and Player
│   │   └── services/         # Domain service: matcher logic
│   ├── ports/                # Hexagonal architecture ports: interfaces
│   ├── use_cases/            # Application layer: orchestrates domain logic
│   └── main.py               # FastAPI app entrypoint
├── scripts/                  # Misc scripts (e.g. for DB seeding)
├── tests/                    # All test modules
└── utils/                    # Utility functions 
```

### Design Highlights

- **Hexagonal Architecture**: clear separation between domain logic and external systems (like databases and APIs)
- **DDD Tactics**: domain models are pure and expressive using pydantic
- **Testability**: domain logic can be tested independently from infrastructure
- **Stub API**: usedd for campaigns to allow fast local testing without network dependencies

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/cosxp2/gameloft-profile-matcher-service.git
cd gameloft-profile-matcher-service
```

### 2. Set Up the Virtual Environment

```bash
pipenv install
pipenv shell
```

### 3. Seed the Database

To populate the database with a test player:

```bash
python -m scripts.load_test_player
```

> This will insert a player into the SQLite `test.db`.

### 4. Start the FastAPI Server

In a new terminal:

```bash
uvicorn app.main:app --reload
```

Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API using the interactive UI.

### 5. Example API Call

Once the server is running and DB is seeded, make a GET request:

```
GET /get_client_config/test_player
```

It should return a valid player profile JSON with matched campaigns (if any).

### 6. Run Tests

```bash
pytest
```

---

## Design Decisions

### Why Hexagonal Architecture + DDD?

- Best for modularity and testability
- Ports and adapters make it easy to swap implementations (e.g., from SQLite to PostgreSQL or a real Campaign API)
- DDD focuses on modeling the business logic explicitly and cleanly

### Why pydantic?

- Ensures runtime validation of data 
- Provides easy functons like `model_copy()` and `model_dump()` for manipulating models immutably
- Strong integration with FastAPI

### Why FastAPI?

- Great fit for microservices and domain-heavy applications
- Good for prorotyping
- Fast serialization/deserialization

### Why SQLite?

- Lightweight and zero configuration, making local testing very easy
- No external server dependency needed during development or for unit/integration testing
- Can be easily swapped later with PostgreSQL via SQLAlchemy (thanks to the adapter abstraction)

---

## Final note
This project is designed with scalability and maintainability in mind, making it production-ready with minimal changes (e.g., switching to a real DB or real API adapter for the campaing fetcher).
