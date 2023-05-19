import flask

app = flask.Flask(__name__)


def create_app():
    from . import controllers

    return app
