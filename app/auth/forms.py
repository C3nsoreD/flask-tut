from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
# import email_validator
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])

    password = PasswordField('Password', validators=[Required()])
    remeber_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', 
        validators=[Required(), Length(1, 64), 
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                'Usernames must have only letters, numbers, dots or underscores')])

    password = PasswordField('Password', validators = [
            Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    # Custom email validation
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in registered')

    
    def validate_username(self, field):
        if User.query.filter_by(usenrmae=field.data).first():
            raise ValidationError('Username already in registered')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password', vaidators=[
        Required(), EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')

class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('New Password', vaidators=[
        Required(), EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unkown email address')


class ChangeEmailForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])

    submit = SubmitField('Update Email address')

    def  validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')