from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth 
from .forms import LoginForm, RegistrationForm
from ..models import User
from ..email import send_mail


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # if form is valid
        # Search for user in database
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


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, 
                    username=form.username.data,
                    passward=form.passward.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confimation_token()
        send_mail(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation has been sent to your email')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks')
    else:
        flash('The confirmation link is invalid or expired.')
    return render_template(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confimation_token()
    send_mail(user.email, 'Confirm Your Account', 'auth/email/confirm', user, token=token)
    flash('A confirmation has been sent to your email')
    return render_template(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticateed() \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect('main.index') 
    
    return render_template('auth/unconfirmed.html')