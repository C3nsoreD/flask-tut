from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User 

@main.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        # check if the user is known
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            # send mail to admin
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

        return redirect(url_for('.index')) # same as: redirect(url_for('main.index'))

    return render_template('index.html', 
        current_time=datetime.utcnow(), 
        form=form, name=session.get('name'),
        known = session.get('known', False))
