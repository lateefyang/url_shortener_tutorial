from . import urlshort
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'ajsdlkfjklmvlkawef'
    app.register_blueprint(urlshort.bp)
    return app
