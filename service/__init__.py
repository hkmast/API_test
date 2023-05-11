import flask

app = flask.Flask(__name__)

def create_app():

    init_models()
    init_controllers()

    return app

def init_controllers():
    print("init controllers...")
    from . import controllers
    print("init controllers done")

def init_models():
    print("init models...")
    from . import models
    print("init models done")