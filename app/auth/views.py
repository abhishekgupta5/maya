#app/auth/views.py

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm
from ..models import User


#Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Handle requests to the /auth/login route.
    Log a user in through login form
    '''
    form = LoginForm()
    #For POST requests
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
    '''
    Handle requests to the /auth/logout route.
    Log a user out and remove/reset the user session
    '''
    logout_user()
    flash("You've successfully logged out")
    #Redirect to login page
    return redirect(url_for('auth.login'))
