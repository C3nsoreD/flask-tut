from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import auth 
from .forms import LoginForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # if form is valid
        # Search for user in databse
        user = User.query.filter_by(email=form.email.data).first()
        # If the user is None and the passward is verified
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data) # Login the user 
            # Return the user to the home page
            return redirect(url_for('main.index'))
        # Otherwise show error
        flash('Invalid username or password')
    # Always render login template
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

