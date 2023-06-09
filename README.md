# CFChemAPI

## Requirements

* Docker
* Docker Compose
* Docker Desktop (Windows)

## Installation

* copy `.env.example` to `.env`
* edit the `.env` credentials to point to the database
* run `docker-compose up --build`
* The API should now be accessible from `localhost:8000`

## Routes

* `/api/v1` - Hello, World (Index)
    * `/lincs (?limit=10&offset=0)` - Get all lincs from DB (default: limit 10 & offset 0)