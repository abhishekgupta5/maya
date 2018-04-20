#app/auth/views.py

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from .. import db
from ..models import User
from ..email import send_email

#Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Handle requests to the /auth/login route.
    Log a user in through login form
    '''
    form = LoginForm()
    #Validate for POST requests
    if form.validate_on_submit():
        #Check whether user exists in db and password matches
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            #Redirect to home page after successful login
            return redirect(request.args.get('next') or url_for('home.homepage'))
        #If login credentials are incorrect
        else:
            flash('Invalid email or password')
    #For GET requests, load login template
    return render_template('auth/login.html', form=form)

#Logout route
@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /auth/logout route.
    Log a user out and remove/reset the user session
    """
    logout_user()
    flash("You've successfully logged out")
    #Redirect to login page
    return redirect(url_for('auth.login'))

#Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to /auth/register route.
    Register a user
    """
    form = RegisterForm()
    #Validate for POST requests
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        #Sending confirmation link via email
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        #Redirect to login page
        return redirect(url_for('auth.login'))
    #For GET requests, return register.html template
    return render_template('auth/register.html', form=form)

#Confirm email route
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.is_confirmed:
        return redirect(url_for('home.homepage'))
    if current_user.confirm(token):
        flash('Your account is confirmed. Thanks.')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('home.homepage'))

#Resend confirmation mail
@auth.route('/confirm')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation mail has been sent to you by email.')
    return redirect(url_for('home.homepage'))

#Handling unconfirmed users
@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.is_confirmed and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.is_confirmed:
        return redirect(url_for('home.homepage'))
    return render_template('auth/unconfirmed.html')

#Change logged in users' password
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('home.homepage'))
        else:
            flash('Invalid Password')
    return render_template("auth/change_password.html", form=form)

#Reset password
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('home.homepage'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset your password', 'auth/email/reset_password', user=user, token=token, next=request.args.get('next'))
        flash('An email with instructions to reset your password has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('home.homepage'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('home.homepage'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('home.homepage'))
    return render_template('auth/reset_password.html', form=form)

#Change registered email
@auth.route('/change-email', methods=['GET','POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address.', 'auth/email/change_email', user=current_user, token=token)
            flash('An email with instructions to confirm your new email has been sent to you.')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid email or password')
    return render_template('auth/change_email.html', form=form)

@auth.route('change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('auth.login'))
