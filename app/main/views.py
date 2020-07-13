from datetime import datetime
from flask import render_template, session, redirect, url_for, flash

from . import main
from .forms import NameForm, EditProfileForm
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


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


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


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)