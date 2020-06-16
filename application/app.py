from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request, make_response
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField 
from wtforms.validators import Required
from datetime import datetime


app = Flask(__name__) 
app.config['SECRET_KEY'] = 'c3n_code'
Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if  form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        # name = form.name.data
        return redirect(url_for('index'))

    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500

#Froms ----------------------->
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField("Submit")


if __name__ == "__main__":
    app.run(debug=True)
Form