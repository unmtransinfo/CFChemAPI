# CFChemAPI

API for fetching data from [CFDE Chemical Database (CFChemDb)](https://github.com/unmtransinfo/CFChemDb).

## Requirements

- Docker
- Docker Compose

## Setup (Development/Local)

1. Copy `app/.env.example` to `app/.env`
2. Edit the `app/.env` credentials to point to the `cfchem` database
3. Run `docker compose --env-file ./app/.env -f docker-compose.dev.yml up --build`

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

#### Code Formatting with Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) hooks to automatically format Python code with [Black](https://black.readthedocs.io/) before each commit. This ensures consistent code style across the project.

**Setup (one-time):**

1. Setup and activate a Python (v3.14) virtual environment if you haven't already:

   ```bash
   conda create -n cfchem-api python=3.14 && conda activate cfchem-api
   ```

2. Install dependencies:

   ```bash
   pip install -r app/requirements.txt
   ```

3. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```

**Usage:**

Once installed, the hooks will run automatically on `git commit`. If Black reformats any files, the commit will be aborted and you'll need to:

1. Review the changes Black made
2. Stage the reformatted files: `git add <files>`
3. Commit again: `git commit`

**Manual formatting:**

You can also run Black manually on all files:

```bash
black .
```

Or run all pre-commit hooks manually without committing:

```bash
pre-commit run --all-files
```

**Configuration:**

- Pre-commit hooks are configured in [.pre-commit-config.yaml](.pre-commit-config.yaml)

## Documentation

- A full set of Swagger documentation can be found at http://localhost:8000/apidocs

## Setup (Production on Chiltepin)

1. **Pull latest changes (for compose file mainly):**

```bash
git pull
```

2. **Copy [.env.prod.example](.env.prod.example) to `.env`**:

```bash
cp .env.prod.example .env
```

3. **Modify `.env`**

4. **(If significant changes to compose file):**

   ```bash
   docker compose -f docker-compose.prod.yml down
   ```

5. **Pull latest images and run:**

   ```bash
   docker compose -f docker-compose.prod.yml pull
   docker compose -f docker-compose.prod.yml up -d --remove-orphans
   ```

6. **Verify deployment:**

   ```bash
   docker compose -f docker-compose.prod.yml ps
   docker compose -f docker-compose.prod.yml logs api
   ```

7. **(One-time setup) If not done so already, modify your /etc/apache2/sites-available/ files to include the following lines**

```
   # cfchem
   ProxyPass /cfchem/api http://localhost:<APP_PORT>/api
   ProxyPassReverse /cfchem/api http://localhost:<APP_PORT>/api
   ProxyPass /cfchem/apidocs/ http://localhost:<APP_PORT>/apidocs/
   ProxyPassReverse /cfchem/apidocs/ http://localhost:<APP_PORT>/apidocs/
   ProxyPass /cfchem/flasgger_static/ http://localhost:<APP_PORT>/cfchem/flasgger_static/
   ProxyPassReverse /cfchem/flasgger_static/ http://localhost:<APP_PORT>/cfchem/flasgger_static/

   # Static directory aliases (e.g., SPA UI builds)
   # cfchem
   Alias /cfchem /var/www/cfchem/

    <Directory /var/www/cfchem/>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted

        # SPA fallback: if the file/dir doesn't exist, serve index.html
        RewriteEngine On
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule ^ index.html [L]
   </Directory>
```

Then reload apache:

```bash
sudo apache2ctl configtest # make sure syntax ok
sudo systemctl reload apache2
curl -I https://chiltepin.health.unm.edu/cfchem/apidocs/ # should give HTTP/1.1 200
```
