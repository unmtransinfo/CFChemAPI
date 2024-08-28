# Badapple2-API
API for Badapple2. Currently in development (do not use for production!)

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
