#app/auth/views.py

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import auth
from .forms import LoginForm
from ..models import User



#@auth.route('/login')
#def login():
#    return render_template('auth/login.html')

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
            return redirect(request.args.get('next') or url_for('main.index'))
        #If login credentials are incorrect
        else:
            flash('Invalid email or password')
    #For GET requests, load login template
    return render_template('auth/login.html', form=form)
