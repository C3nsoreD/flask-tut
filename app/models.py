from flask_sqlalchemy import SQLAlchemy
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

### Models ---------------------->
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return f'<User {self.name}>'
    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def password(self):
        '''
        Password property to prevent reading passwords directly
        '''
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        '''
        Password setter. Applies hashing to the password
        '''
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    '''
    This sets the callback for reloading a user from the session.
    '''
    return User.query.get(int(user_id))
