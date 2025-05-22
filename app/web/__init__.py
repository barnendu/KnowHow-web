from flask import Flask
from flask_cors import CORS
from app.web.config import Config
from app.celery import celery_init_app
from app.web.db import db, init_db_command
from app.web.hooks import (
    load_logged_in_user,
    add_headers,
    handle_error
)

from app.web.views import (
    auth_views,
    client_views,
    doc_views,
    conversation_views,
    integrated_views
)

def create_app():
    app = Flask(__name__, static_folder="../../client/build")
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    register_db(app)
    register_hooks(app)
    register_blueprint(app)
    if Config.CELERY["broker_url"]:
        celery_init_app(app)
    return app

def register_db(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)

def register_blueprint(app):
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(client_views.bp)
    app.register_blueprint(doc_views.bp)
    app.register_blueprint(conversation_views.bp)
    app.register_blueprint(integrated_views.bp)

def register_hooks(app):
    CORS(app)
    app.before_request(load_logged_in_user)
    app.after_request(add_headers)
    app.register_error_handler(Exception, handle_error)
