# HierS-API

## Requirements

* Docker
* Docker Compose

## Installation (Development)

* copy `.env.example` to `.env`
* edit the `.env` credentials as needed
* run `docker-compose -f compose-development.yml up --build`
* The API should now be accessible from `localhost:8000`

## Documentation

* A full set of Swagger documentation can be found at http://localhost:8000/apidocs

## Routes

* `/api/v1` - Hello, World (Index)
    * `/lincs (?limit=10&offset=0)` - Get all lincs from DB (default: limit 10 & offset 0)
