from flask_script import Manager, Server
from sqlalchemy_utils.functions import create_database,drop_database
from hello.app import create_app
from hello.common.database import db

app = create_app()
manager = Manager(app)

@manager.command
def db_create():
    create_database(app.config.get('SQLALCHEMY_DATABASE_URI'))
    with app.app_context():
        db.create_all()

@manager.command
def db_drop():
    drop_database(app.config.get('SQLALCHEMY_DATABASE_URI'))

manager.add_command('runserver', Server(host='0.0.0.0', port=5000))

if __name__ == '__main__':
    manager.run()
