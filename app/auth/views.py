from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user

from . import auth 
from .forms import LoginForm
from ..models import User

@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.passwoord.data):
            login_user(User, form.remeber_me.data)
            
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password')

    return render_template('auth/login.html', form=form)