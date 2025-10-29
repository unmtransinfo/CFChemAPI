# CFChemAPI

API for fetching data from [CFDE Chemical Database (CFChemDb)](https://github.com/unmtransinfo/CFChemDb).

## TODO

- (For production) add internal network in compose file
- Clean up API Spec

## Requirements

- Docker
- Docker Compose

## Setup (Development/Local)

1. Copy `app/.env.example` to `app/.env`
2. Edit the `app/.env` credentials to point to the `cfchem` database
3. Run `docker compose -f compose-development.yml up --build`

The API should now be accessible from `localhost:8000`

### Development Notes

#### Upgrading Dependencies

If one finds they need to update dependencies (`requirements.txt`), the following steps can be followed:

1. If a new package is required, add it to `requirements.in`
2. Setup and activate a Python (v3.14) virtual environment. For example, with conda use:
   ```
   conda create -n cfchem-api python=3.14 && conda activate cfchem-api
   ```
3. Install pip-tools: `pip install pip-tools`
4. Compile new requirements: `pip-compile --upgrade`
   - Make sure you are in the `app/` directory: `cd app/`
5. (Optional) Test the update locally in your environment: `pip-sync`

_Note_: If you need to update the Python version, make sure to adjust the steps above accordingly and to update the Python image in `Dockerfile`.

## Documentation

- A full set of Swagger documentation can be found at http://localhost:8000/apidocs

## Setup (Production on Chiltepin)

1. Copy [production_env.example](production_env.example) to `.env`: `cp production_env.example .env`
2. Fill in/edit the `.env` credentials as needed
3. Update apache2 config:
   - Create a new file for apache2 config: `/etc/apache2/sites-available/cfchemapi.conf`
   - Add the following line to `/etc/apache2/apache2.conf`:
     ```
     Include /etc/apache2/sites-available/cfchemapi.conf
     ```
   - Update the apache2 virtual config file: `/etc/apache2/sites-enabled/000-default.conf`
   - Run config check: `sudo apachectl configtest`
   - (If config check passed) reload apache: `sudo systemctl reload apache2`
4. (If server was previously up): `docker-compose down`
5. Run `docker-compose up --build -d`
