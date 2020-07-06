from flask import (
    Flask, render_template, session, redirect, url_for, flash)
from flask import request, make_response

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail

from flask_wtf import Form
from wtforms import StringField, SubmitField 
from wtforms.validators import Required

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Message
from datetime import datetime

import os
from threading import Thread


basebir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)

### Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basebir, 'data.sqlite')
# app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = 'c3n_code'

app.config['MAIL_SERVER'] = 'stmp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') # FixMe - change to export MAIL_USERNAME='my_mail'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') # FixMe - change to export MAIL_PASSWORD='my_password'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Blog2.0]'
app.config['FLASKY_MAIL_SENDER'] = 'Blog2.0 Admin <blogtwo@example.com>'
app.config['BLOG_TWO_ADMIN'] = os.environ.get('BLOG_TWO_ADMIN')

### extention init
Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
db.app = app
migrate = Migrate(app, db)
mail = Mail(app)

### Utility functions
def send_mail(to, subject, template, **kwargs):
    # sending mail abstraction 
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
                sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def init_db():
    db.create_all()

    # Create a test user
    new_user = User('a@a.com', 'user_role')
    # new_user.display_name = 'Nathan'
    db.session.add(new_user)
    db.session.commit()

    # new_user.datetime_subscription_valid_until = datetime.datetime(2019, 1, 1)
    db.session.commit()


### Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        # check if the user is known
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['BLOG_TWO_ADMIN']:
                send_mail(
                    app.config['BLOG_TWO_ADMIN'], # to 
                    'New User', # subject
                    'mail/new_user', # template folder
                    user=user # kwargs for the template file
                    )
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('index'))

    return render_template('index.html', current_time=datetime.utcnow(), 
            form=form, name=session.get('name'), known = session.get('known' , False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


### Froms ----------------------->
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField("Submit")



if __name__ == "__main__":
    db.create_all()
    init_db()
    app.run(debug=True)