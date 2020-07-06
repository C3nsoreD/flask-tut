from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length
# import email_validator


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])

    password = PasswordField('Pssword', validators=[Required()])
    remeber_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

