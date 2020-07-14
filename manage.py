import os 
from app import create_app, db
from app.models import User, Role, Permission
import click 
from flask.cli import AppGroup

from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

# add shell arguments for flask shell instance 
@app.shell_context_processor
def make_shell_context():
    """
    Registers objects from the app.
    For quick db testing and configurations. Saves time
    
    Ex: >>> u = User(username='john', password='cat')
    """
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission)

# Registered command line argument `test`
@app.cli.command()
def test():
    """Run the unit tests."""

    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)