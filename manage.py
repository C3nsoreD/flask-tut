import os 
from app import create_app, db
from app.models import User, Role
import click 
from flask.cli import AppGroup

from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') of 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


    