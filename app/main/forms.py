from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField 
from wtforms.validators import Required
from . import main

### Froms ----------------------->
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField("Submit")
