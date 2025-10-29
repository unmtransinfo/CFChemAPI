FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# ENV vars can be overridden by docker compose / .env file
ENV APP_PORT=8000
ENV N_WORKERS=3
ENV MAX_REQUESTS=1000
CMD echo "RUNTIME: APP_PORT=${APP_PORT}, N_WORKERS=${N_WORKERS}, MAX_REQUESTS=${MAX_REQUESTS}" && gunicorn --bind "0.0.0.0:${APP_PORT}" --workers ${N_WORKERS} --max-requests ${MAX_REQUESTS} --reload app:app