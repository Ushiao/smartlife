# -*- coding:utf-8 -*-

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

from . import smartlife


DEFAULT_MODULES = (
    (smartlife, "/smartlife"),
)


def create_app(debug=False):
    app = Flask(__name__)
    app.debug=debug
    app.config['SECRET_KEY'] = 'fajio10g90sf67#'

    for module, url_prefix in DEFAULT_MODULES:
        app.register_blueprint(module.main, url_prefix=url_prefix)
    socketio.init_app(app)
    return app
