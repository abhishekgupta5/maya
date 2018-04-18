#app/auth/views.py

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from . import auth
from .forms import LoginForm, RegisterForm
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
        return redirect(url_for('home.homepage'))
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
