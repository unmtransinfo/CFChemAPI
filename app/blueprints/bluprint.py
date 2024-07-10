from flask import Blueprint

test_bluprint = Blueprint("test_bluprint", __name__, url_prefix="/test_bluprint")


@test_bluprint.route("/")
def index():
    x = "TEST"
    return f"{x} : BluPrint registered!"
