from flask import Flask
from hello.common.database import db, replicated
from hello.config import ContainerConfig
from hello.api import blueprint as api

def create_app():
    app = Flask(__name__)
    app.config.from_object(ContainerConfig())
    app.register_blueprint(api)
    db.init_app(app)
    replicated.init_app(app)
    return app
