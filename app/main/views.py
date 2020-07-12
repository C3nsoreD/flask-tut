from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from flask_login import login_required, current_user
from ..models import User, Permission
from ..decorators import admin_required, permission_required


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
            # if app.config['BLOG_TWO_ADMIN']:
            #     send_mail(
            #         app.config['BLOG_TWO_ADMIN'], # to 
            #         'New User', # subject
            #         'mail/new_user', # template folder
            #         user=user # kwargs for the template file
            #         )
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('.index')) # same as: redirect(url_for('main.index'))

    return render_template('index.html', 
        current_time=datetime.utcnow(), 
        form=form, name=session.get('name'),
        known = session.get('known', False))

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators only"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For moderators only"


