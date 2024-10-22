# Badapple2-API
API code for Badapple2. Currently in beta. 

The `compose-production.yml` file will spin up the Badapple2 website (DB, API, and UI). 

## Requirements

* Docker
* Docker Compose

## Setup (Development)
1. Copy `.env.example` to `.env` (in the `/app` folder)
2. Edit the `.env` credentials as needed
3. Run `docker-compose --env-file ./app/.env -f compose-development.yml up --build`
    * Note: Depending on your version of docker, you may instead want to use: `docker compose --env-file ./app/.env -f compose-development.yml up --build`
4. The API should now be accessible from `localhost:8000`
   * A full set of Swagger documentation can be found at http://localhost:8000/apidocs

## Setup (Production on Chiltepin)
1. Copy `production_env.example` to `.env`
2. Fill in/edit the `.env` credentials as needed
3. Run `docker-compose -f compose-production.yml up --build`

