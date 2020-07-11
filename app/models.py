from flask_sqlalchemy import SQLAlchemy
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


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
    confirmed = db.Column(db.Boolean, default=False)
    
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

    # User account confirmantion
    def generate_confirmation_token(self, expiration=3600):
        '''
        Returns a dictionary from comfimation 
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})

    def generate_reset_token(self, expiration=3600):
        '''
        Returns a dictionary for resets
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset':self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email':new_email})
 
    def confirm(self, token):
        '''
        Confirm function: Used for verify if the Token is authenticate.
        Used for Email confirmation messages.
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False 
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def change_email(self, token):
        '''
        Takes a authenticaton token verifies token using SECRET_KEY if the token is valid a new email is recorded.
        Checks if the new email already exists in the db. 
        Returns True if the email is unique and the token is authentic. 
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        
        new_email = data.get('new_email')
        if new_email is None:
            return False 
        # If the new email already exists in the database
        # return False 
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        
        return True
         
    def reset_password(self, token, new_password):
        '''
        Takes 2 arguments. A token and new password, Verifies the token
        Adds new password to the database.
        Returns True if token is authentic
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True



@login_manager.user_loader
def load_user(user_id):
    '''
    This sets the callback for reloading a user from the session.
    '''
    return User.query.get(int(user_id))
