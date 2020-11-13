import os

import click
from flask import Flask, render_template

from app.extensions import db, login_manager, csrf
from settings import config


def register_blueprints(app):
    from app.blueprints.todo import todo_bp
    from app.blueprints.auth import auth_bp
    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_commands(app):
    @app.cli.command()
    def initdb():
        '''init db'''
        import app.models
        db.create_all()
        click.echo('Initialized database.')
