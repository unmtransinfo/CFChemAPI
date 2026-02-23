# blueprints/health.py

from flask import Blueprint, jsonify

health = Blueprint("health", __name__, url_prefix="/health")


@health.route("/", methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok"})
