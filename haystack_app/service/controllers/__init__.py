from service import app
from . import search_controller

@app.route("/ping", methods=["POST", "GET"])
def ping():
    return "pong"