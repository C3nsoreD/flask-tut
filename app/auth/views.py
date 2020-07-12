from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth 
from .forms import (
    LoginForm, RegistrationForm, ChangePasswordForm, ChangeEmailForm, PasswordResetRequestForm
)
from ..models import User
from ..email import send_mail


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # if form is valid
        # Search for user in database
        user = User.query.filter_by(email=form.email.data).first()
        # If the user is None and the password is verified
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
                    password=form.password.data)
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

# User must be logged-in inorder to recieve another confirmation email
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A confirmation has been sent to your email')
    return redirect(url_for('main.index'))

# before each request a user is verified if they have confirmed there email
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

# Route for unconfirmed user 
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index') 
    
    return render_template('auth/unconfirmed.html')

# Account management
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # old password verification
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password')
    render_template('auth/change_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_confimation_token(new_email)
            send_mail(new_email, 'Confirm your email address', 
                        'auth/email/change_email', user=current_user, token=token
            )
            flash('An email with instructions has been sent to your new email address. Please confirm it!')
            redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')
    
    return render_template('auth/change_email.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    # if the current user is ananymous
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Send a security token to registered user 
        if user:
            token = user.generate_confimation_token()
            send_mail(user.email, 'Reset Your Password',
                    'auth/email/reset_password',
                    user=user, token=token,
                    next=request.args.get('next'))
            flash('An email with instructions to reset your password has been sent to you')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check is the user object belongs to sessions
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
