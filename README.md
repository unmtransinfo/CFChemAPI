# CFChemAPI

## Requirements

* Docker
* Docker Compose
* Docker Desktop (Windows)

## Installation

* copy `.env.example` to `.env`
* edit the `.env` credentials to point to the database
* run `docker-compose -f compose-development.yml up --build`
* The API should now be accessible from `localhost:8000`

## Documentation

* A full set of Swagger documentation can be found at http://localhost:8000/apidocs

## Routes

* `/api/v1` - Hello, World (Index)
    * `/lincs (?limit=10&offset=0)` - Get all lincs from DB (default: limit 10 & offset 0)

## Deployment

### Basic deployment (Easiest):
* Copy `.env.example` to `.env`
* Run `docker compose up`

#### Notes
* You should create a cron job to back up ./db regularly. You can tar the directory or use mysqldump (https://dev.mysql.com/doc/refman/8.3/en/mysqldump.html) along with the mysql container. (ex: `docker compose exec mysql mysqldump [options] > dump.sql`)

### Recommended (Requires external MySql database):

* Copy `.env.example` to `.env`
* Edit .env to have connection information for an external database
* Run `docker compose up`

### Note
* The docker compose file comes with a Mysql database however, it is recommended to use an external Mysql database. To connect to an external database, copy the .env.example file to .env and edit the variables.

* If you decide to use the internal database the datastore location can be changed with DATABASE_VOLUME_PATH (default ./db)