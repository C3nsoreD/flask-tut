from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import Required, Length
from . import main

### Froms ----------------------->
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField("Submit")

class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextField('About me')
    submit = StringField('Submit')
