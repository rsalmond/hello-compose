import flask_sqlalchemy
import flask_replicated

db = flask_sqlalchemy.SQLAlchemy()
replicated = flask_replicated.FlaskReplicated()
